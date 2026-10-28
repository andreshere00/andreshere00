import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from conftest import PROJECT_ROOT, make_docx

# ---- Mocks, fixtures & helpers ---- #

SCRIPT: Path = PROJECT_ROOT / "skills/local/doc-diff/scripts/diff_docs.py"


@pytest.fixture(scope="module")
def diff_docs() -> ModuleType:
    spec = importlib.util.spec_from_file_location("diff_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---- Happy path ---- #


def test_compare_modified_paragraph_reports_word_level_change(diff_docs, tmp_path: Path):
    old = make_docx(tmp_path / "a.docx", ["Payment is due in 30 days."], heading="Terms")
    new = make_docx(tmp_path / "b.docx", ["Payment is due in 45 days."], heading="Terms")

    changes = diff_docs.compare(diff_docs.extract_blocks(old), diff_docs.extract_blocks(new))

    assert [c["op"] for c in changes] == ["changed"]
    assert changes[0]["diff"] == "Payment is due in [-30-]{+45+} days."


def test_compare_deleted_paragraph_is_reported_as_removed(diff_docs, tmp_path: Path):
    old = make_docx(tmp_path / "a.docx", ["Alpha.", "Beta.", "Gamma."])
    new = make_docx(tmp_path / "b.docx", ["Alpha.", "Gamma."])

    changes = diff_docs.compare(diff_docs.extract_blocks(old), diff_docs.extract_blocks(new))

    assert changes == [{"op": "removed", "old_index": 2, "old": "Beta."}]


def test_compare_inserted_paragraph_is_reported_as_added(diff_docs, tmp_path: Path):
    old = make_docx(tmp_path / "a.docx", ["Alpha.", "Gamma."])
    new = make_docx(tmp_path / "b.docx", ["Alpha.", "Beta.", "Gamma."])

    changes = diff_docs.compare(diff_docs.extract_blocks(old), diff_docs.extract_blocks(new))

    assert changes == [{"op": "added", "new_index": 2, "new": "Beta."}]


def test_main_markdown_output_summarises_counts(diff_docs, tmp_path: Path, capsys):
    old = make_docx(tmp_path / "a.docx", ["One.", "Two."])
    new = make_docx(tmp_path / "b.docx", ["One.", "Two.", "Three."])

    exit_code = diff_docs.main([str(old), str(new)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "0 changed, 1 added, 0 removed" in output
    assert "ADDED (new #3): Three." in output


def test_main_json_format_outputs_machine_readable_changes(diff_docs, tmp_path: Path, capsys):
    old = make_docx(tmp_path / "a.docx", ["One."])
    new = make_docx(tmp_path / "b.docx", ["One.", "Two."])

    diff_docs.main([str(old), str(new), "--format", "json"])

    changes = json.loads(capsys.readouterr().out)
    assert changes == [{"op": "added", "new_index": 2, "new": "Two."}]


def test_unified_hunks_edited_line_pairs_delete_and_insert_with_word_segments(diff_docs):
    old = ["a", "b", "Pay in 30 days.", "d", "e"]
    new = ["a", "b", "Pay in 45 days.", "d", "e"]

    hunks = diff_docs.unified_hunks(old, new, context=1)

    assert len(hunks) == 1
    assert (hunks[0]["old_start"], hunks[0]["old_count"]) == (2, 3)
    assert [line["type"] for line in hunks[0]["lines"]] == [
        "context",
        "delete",
        "insert",
        "context",
    ]
    deleted = hunks[0]["lines"][1]
    assert [(s["kind"], s["text"]) for s in deleted["segments"]] == [
        ("equal", "Pay in "),
        ("delete", "30"),
        ("equal", " days."),
    ]


def test_main_unified_format_prints_git_style_headers(diff_docs, tmp_path: Path, capsys):
    old = make_docx(tmp_path / "a.docx", ["One."])
    new = make_docx(tmp_path / "b.docx", ["One.", "Two."])

    diff_docs.main([str(old), str(new), "--format", "unified"])

    output = capsys.readouterr().out
    assert output.startswith("--- a.docx\n+++ b.docx\n@@ -1,2 +1,3 @@")
    assert "+Two." in output


# ---- Error paths ---- #


def test_main_missing_file_returns_exit_code_two(diff_docs, tmp_path: Path, capsys):
    exit_code = diff_docs.main([str(tmp_path / "nope.docx"), str(tmp_path / "nope2.docx")])

    assert exit_code == 2
    assert "file not found" in capsys.readouterr().err


# ---- Edge cases ---- #


def test_compare_identical_documents_reports_no_differences(diff_docs, tmp_path: Path, capsys):
    old = make_docx(tmp_path / "a.docx", ["Same text."])
    new = make_docx(tmp_path / "b.docx", ["Same text."])

    diff_docs.main([str(old), str(new)])

    assert "No differences found." in capsys.readouterr().out


def test_extract_blocks_table_rows_are_rendered_as_markdown_cells(diff_docs, tmp_path: Path):
    doc = make_docx(tmp_path / "a.docx", ["Intro"])

    blocks = diff_docs.extract_blocks(doc)

    assert blocks == ["Intro", "| Price | 100 |"]


def test_extract_blocks_heading_style_becomes_markdown_prefix(diff_docs, tmp_path: Path):
    doc = make_docx(tmp_path / "a.docx", [], heading="Title")

    assert diff_docs.extract_blocks(doc)[0] == "# Title"


def test_extract_blocks_plain_text_file_is_split_into_lines(diff_docs, tmp_path: Path):
    path = tmp_path / "notes.txt"
    path.write_text("a\nb\n")

    assert diff_docs.extract_blocks(path) == ["a", "b"]


def test_unified_hunks_pure_insertion_has_no_word_segments(diff_docs):
    hunks = diff_docs.unified_hunks(["a"], ["a", "b"])

    inserted = [line for line in hunks[0]["lines"] if line["type"] == "insert"]
    assert [line["text"] for line in inserted] == ["b"]
    assert "segments" not in inserted[0]
    assert inserted[0]["new_no"] == 2


def test_unified_hunks_distant_changes_are_split_into_separate_hunks(diff_docs):
    old = [str(i) for i in range(30)]
    new = list(old)
    new[2], new[27] = "X", "Y"

    assert len(diff_docs.unified_hunks(old, new, context=2)) == 2


def test_unified_hunks_identical_documents_return_no_hunks(diff_docs):
    assert diff_docs.unified_hunks(["a", "b"], ["a", "b"]) == []
