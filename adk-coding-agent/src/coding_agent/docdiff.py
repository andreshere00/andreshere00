import importlib.util
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Any

from coding_agent.sandbox import SandboxEnvironment
from coding_agent.skills import SkillRepository

DOC_CONTEXT_KEY: str = "doc_context"
COMPARABLE_SUFFIXES: frozenset[str] = frozenset({".docx", ".txt", ".md"})
MAX_CONTEXT_CHARS: int = 60_000
SCRIPT_PATH: Path = Path("doc-diff") / "scripts" / "diff_docs.py"


@cache
def _load(script: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("doc_diff_skill", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocumentComparer:
    """Compares and describes documents using the `doc-diff` skill script.

    The skill script is the single implementation of the diff, so the UI, the HTTP API and the
    agent running the script in its sandbox always agree.
    """

    def __init__(self, repository: SkillRepository, environment: SandboxEnvironment) -> None:
        """Initializes the comparer.

        Args:
            repository: Skills repository providing the `doc-diff` skill.
            environment: Workspace the documents live in; also enforces the path jail.
        """
        self._script = repository.local_dir / SCRIPT_PATH
        self._env = environment

    def _resolve(self, name: str) -> Path:
        path = self._env.resolve(name)
        if path.suffix.lower() not in COMPARABLE_SUFFIXES or not path.is_file():
            raise FileNotFoundError(f"Document not found or unsupported: {name}")
        return path

    def compare(self, old_name: str, new_name: str, context: int = 3) -> dict[str, Any]:
        """Builds a git-style comparison of two documents.

        Args:
            old_name: Workspace path of the original document.
            new_name: Workspace path of the revised document.
            context: Unchanged blocks shown around each change.

        Returns:
            Names, change counts (`changed`, `added`, `removed`) and `hunks` with word-level
            segments.

        Raises:
            PermissionError: If a path escapes the workspace.
            FileNotFoundError: If a document is missing or has an unsupported type.
        """
        diff = _load(self._script)
        old_blocks = diff.extract_blocks(self._resolve(old_name))
        new_blocks = diff.extract_blocks(self._resolve(new_name))
        changes = diff.compare(old_blocks, new_blocks)
        return {
            "old": old_name,
            "new": new_name,
            "old_blocks": len(old_blocks),
            "new_blocks": len(new_blocks),
            "stats": {
                op: sum(c["op"] == op for c in changes) for op in ("changed", "added", "removed")
            },
            "hunks": diff.unified_hunks(old_blocks, new_blocks, context),
        }

    def build_context(self, old_name: str, new_name: str) -> str:
        """Builds the text the agent needs to answer questions about a document pair.

        Args:
            old_name: Workspace path of the original document.
            new_name: Workspace path of the revised document.

        Returns:
            The numbered text of both documents plus a git-style diff. Each document is
            truncated to `MAX_CONTEXT_CHARS`.

        Raises:
            PermissionError: If a path escapes the workspace.
            FileNotFoundError: If a document is missing or has an unsupported type.
        """
        diff = _load(self._script)
        paths = {"original": self._resolve(old_name), "revised": self._resolve(new_name)}
        blocks = {role: diff.extract_blocks(path) for role, path in paths.items()}
        parts = ["The user is asking about these two versions of a document."]
        for role, path in paths.items():
            numbered = "\n".join(f"[{i}] {text}" for i, text in enumerate(blocks[role], 1))
            if len(numbered) > MAX_CONTEXT_CHARS:
                numbered = numbered[:MAX_CONTEXT_CHARS] + "\n[... truncated ...]"
            parts.append(f'<document role="{role}" file="{path.name}">\n{numbered}\n</document>')
        unified = diff.render_unified(
            paths["original"],
            paths["revised"],
            diff.unified_hunks(blocks["original"], blocks["revised"]),
        )
        parts.append(f"<diff>\n{unified[:MAX_CONTEXT_CHARS]}\n</diff>")
        parts.append(
            "Answer from this text. Cite block numbers like [3] and quote exact wording for "
            "important points. If the answer is not in the documents, say so."
        )
        return "\n\n".join(parts)
