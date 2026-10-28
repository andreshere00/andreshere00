import json
import shutil
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path

from google.adk.skills import Skill, load_skills_from_dir

SOURCES_FILE: str = "sources.toml"
LOCK_FILE: str = ".lock.json"


@dataclass(frozen=True)
class SkillSource:
    """A pinned upstream git repository that provides skills.

    Attributes:
        name: Local label for the source.
        repo: Git URL.
        ref: Commit SHA, tag or branch to pin.
        skills: Skill folder names to import.
        path: Folder inside the repository containing the skill folders.
    """

    name: str
    repo: str
    ref: str
    skills: tuple[str, ...]
    path: str = "skills"


class SkillRepository:
    """Local skills repository with committed skills and pinned third-party skills.

    Layout under `root`:
        local/   skills authored in this project (versioned in git).
        vendor/  skills fetched from upstream sources (git-ignored, see `sources.toml`).
        sources.toml  pinned upstream sources.
        vendor/.lock.json  resolved commit per imported skill.
    """

    def __init__(self, root: Path) -> None:
        """Initializes the repository.

        Args:
            root: Directory containing `local/`, `vendor/` and `sources.toml`.
        """
        self.root = root
        self.local_dir = root / "local"
        self.vendor_dir = root / "vendor"

    def sources(self) -> list[SkillSource]:
        """Reads the pinned upstream sources.

        Returns:
            Sources declared in `sources.toml` (empty when the file is missing).
        """
        manifest = self.root / SOURCES_FILE
        if not manifest.exists():
            return []
        entries = tomllib.loads(manifest.read_text())["source"]
        return [SkillSource(**{**entry, "skills": tuple(entry["skills"])}) for entry in entries]

    def sync(self) -> dict[str, str]:
        """Fetches every declared skill at its pinned ref into `vendor/`.

        Returns:
            Mapping of skill name to the commit SHA that was imported.

        Raises:
            subprocess.CalledProcessError: If a git operation fails.
            FileNotFoundError: If a declared skill is missing from its source.
        """
        lock: dict[str, dict[str, str]] = {}
        self.vendor_dir.mkdir(parents=True, exist_ok=True)
        for source in self.sources():
            with tempfile.TemporaryDirectory() as tmp:
                commit = _fetch(source, Path(tmp))
                for skill in source.skills:
                    origin = Path(tmp) / source.path / skill
                    if not origin.is_dir():
                        raise FileNotFoundError(f"Skill '{skill}' not found in {source.repo}")
                    target = self.vendor_dir / skill
                    shutil.rmtree(target, ignore_errors=True)
                    shutil.copytree(origin, target)
                    lock[skill] = {"repo": source.repo, "commit": commit}
        (self.vendor_dir / LOCK_FILE).write_text(json.dumps(lock, indent=2) + "\n")
        return {name: entry["commit"] for name, entry in lock.items()}

    def load_all(self) -> list[Skill]:
        """Loads every available skill; local skills override vendored ones by name.

        Returns:
            Skills ready to be passed to ADK's `SkillToolset`.
        """
        skills: dict[str, Skill] = {}
        for directory in (self.vendor_dir, self.local_dir):
            if directory.is_dir():
                skills.update({skill.name: skill for skill in load_skills_from_dir(directory)})
        return list(skills.values())


def _fetch(source: SkillSource, destination: Path) -> str:
    """Shallow-fetches `source.ref` into `destination` and returns the resolved commit."""

    def git(*args: str) -> str:
        done = subprocess.run(
            ["git", "-C", str(destination), *args],
            capture_output=True, text=True, check=True,
        )  # fmt: skip
        return done.stdout.strip()

    git("init", "-q")
    git("fetch", "-q", "--depth", "1", source.repo, source.ref)
    git("checkout", "-q", "FETCH_HEAD")
    return git("rev-parse", "HEAD")
