import subprocess
from pathlib import Path

import pytest

from coding_agent.skills import SkillRepository
from conftest import PROJECT_ROOT

# ---- Mocks, fixtures & helpers ---- #


def write_skill(directory: Path, name: str, description: str) -> None:
    folder = directory / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
    )


def git(path: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(path), *args], capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


@pytest.fixture
def upstream(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "upstream"
    write_skill(repo / "skills", "docx", "Upstream docx skill.")
    git(tmp_path, "init", "-q", str(repo))
    git(repo, "add", ".")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    return repo, git(repo, "rev-parse", "HEAD")


def write_sources(root: Path, repo: Path, ref: str, skills: str = '["docx"]') -> None:
    (root / "sources.toml").write_text(
        f'[[source]]\nname = "up"\nrepo = "{repo}"\nref = "{ref}"\nskills = {skills}\n'
    )


# ---- Happy path ---- #


def test_load_all_project_repository_includes_doc_diff_skill():
    names = [skill.name for skill in SkillRepository(PROJECT_ROOT / "skills").load_all()]

    assert "doc-diff" in names


def test_sync_pinned_source_copies_skill_and_writes_lock(tmp_path: Path, upstream):
    repo, commit = upstream
    root = tmp_path / "skills"
    root.mkdir()
    write_sources(root, repo, commit)
    repository = SkillRepository(root)

    resolved = repository.sync()

    assert resolved == {"docx": commit}
    assert [skill.name for skill in repository.load_all()] == ["docx"]
    assert commit in (root / "vendor" / ".lock.json").read_text()


def test_load_all_local_skill_overrides_vendored_skill_with_same_name(tmp_path: Path):
    root = tmp_path / "skills"
    write_skill(root / "vendor", "docx", "vendored")
    write_skill(root / "local", "docx", "local override")

    skills = SkillRepository(root).load_all()

    assert [skill.frontmatter.description for skill in skills] == ["local override"]


# ---- Error paths ---- #


def test_sync_skill_missing_in_source_raises_file_not_found(tmp_path: Path, upstream):
    repo, commit = upstream
    root = tmp_path / "skills"
    root.mkdir()
    write_sources(root, repo, commit, skills='["pptx"]')

    with pytest.raises(FileNotFoundError, match="pptx"):
        SkillRepository(root).sync()


def test_sync_unknown_ref_raises_called_process_error(tmp_path: Path, upstream):
    repo, _ = upstream
    root = tmp_path / "skills"
    root.mkdir()
    write_sources(root, repo, "0" * 40)

    with pytest.raises(subprocess.CalledProcessError):
        SkillRepository(root).sync()


# ---- Edge cases ---- #


def test_sources_missing_manifest_returns_empty_list(tmp_path: Path):
    assert SkillRepository(tmp_path).sources() == []


def test_load_all_empty_repository_returns_no_skills(tmp_path: Path):
    assert SkillRepository(tmp_path).load_all() == []


def test_project_manifest_pins_anthropic_docx_to_a_commit():
    sources = SkillRepository(PROJECT_ROOT / "skills").sources()

    assert [(s.repo, s.skills, len(s.ref)) for s in sources] == [
        ("https://github.com/anthropics/skills", ("docx",), 40)
    ]
