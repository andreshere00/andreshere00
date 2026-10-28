from pathlib import Path

from coding_agent.docdiff import DocumentComparer
from coding_agent.examples import EXAMPLES, seed_examples
from coding_agent.sandbox import ProcessSandbox
from coding_agent.skills import SkillRepository

# ---- Mocks, fixtures & helpers ---- #


def comparer(settings) -> DocumentComparer:
    environment = ProcessSandbox(settings.workspace_dir, timeout=30)
    return DocumentComparer(SkillRepository(settings.skills_dir), environment)


# ---- Happy path ---- #


def test_seed_examples_empty_workspace_creates_all_documents(tmp_path: Path) -> None:
    created = seed_examples(tmp_path)

    assert {path.name for path in created} == set(EXAMPLES)


def test_compare_agreement_versions_reports_changes(settings) -> None:
    settings.workspace_dir.mkdir(parents=True, exist_ok=True)
    seed_examples(settings.workspace_dir)

    result = comparer(settings).compare(
        "examples/service-agreement.v1.docx", "examples/service-agreement.v2.docx"
    )

    assert result["stats"]["changed"] >= 4


# ---- Edge cases ---- #


def test_seed_examples_existing_files_are_not_overwritten(tmp_path: Path) -> None:
    seed_examples(tmp_path)

    assert seed_examples(tmp_path) == []


def test_compare_identical_policy_copies_has_no_hunks(settings) -> None:
    settings.workspace_dir.mkdir(parents=True, exist_ok=True)
    seed_examples(settings.workspace_dir)

    result = comparer(settings).compare(
        "examples/privacy-policy.v1.docx", "examples/privacy-policy.v1-copy.docx"
    )

    assert result["hunks"] == []
