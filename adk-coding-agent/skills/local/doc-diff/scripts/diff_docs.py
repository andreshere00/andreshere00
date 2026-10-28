#!/usr/bin/env python3
"""Compare two versions of a document and report block-level and word-level changes.

Supports .docx (paragraphs, headings and tables, in body order) and any plain-text file.
Text inside tracked insertions is included; tracked deletions are ignored, so the result is
the "accepted changes" view of each file.

Usage:
    python diff_docs.py OLD NEW [--format markdown|json]
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

W_NS: str = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
TOKEN_PATTERN: re.Pattern[str] = re.compile(r"\s+|\S+")


def _text(element) -> str:
    """Concatenates visible text (`w:t`) below an XML element."""
    return "".join(node.text or "" for node in element.iter(f"{{{W_NS}}}t"))


def _heading_prefix(paragraph) -> str:
    """Returns a markdown heading prefix derived from the paragraph style, if any."""
    style = paragraph.find(f"{{{W_NS}}}pPr/{{{W_NS}}}pStyle")
    value = style.get(f"{{{W_NS}}}val", "") if style is not None else ""
    match = re.fullmatch(r"(?i)heading\s*(\d)", value)
    return "#" * int(match.group(1)) + " " if match else ""


def extract_blocks(path: Path) -> list[str]:
    """Extracts comparable text blocks from a document.

    Args:
        path: A .docx file or a plain-text file.

    Returns:
        One string per paragraph or table row (docx), or per line (text files).
    """
    if path.suffix.lower() != ".docx":
        return path.read_text(errors="replace").splitlines()
    from docx import Document

    blocks: list[str] = []
    for child in Document(str(path)).element.body:
        tag = child.tag.removeprefix(f"{{{W_NS}}}")
        if tag == "p":
            text = _text(child)
            if text.strip():
                blocks.append(_heading_prefix(child) + text)
        elif tag == "tbl":
            for row in child.iter(f"{{{W_NS}}}tr"):
                cells = [_text(cell) for cell in row.findall(f"{{{W_NS}}}tc")]
                blocks.append("| " + " | ".join(cells) + " |")
    return blocks


def word_diff(old: str, new: str) -> str:
    """Renders an inline word-level diff using `[-removed-]` and `{+added+}` markers.

    Args:
        old: Original text.
        new: Updated text.

    Returns:
        The merged text with change markers.
    """
    old_tokens, new_tokens = TOKEN_PATTERN.findall(old), TOKEN_PATTERN.findall(new)
    parts: list[str] = []
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":
            parts.append("".join(old_tokens[a0:a1]))
            continue
        if a1 > a0:
            parts.append("[-" + "".join(old_tokens[a0:a1]).strip() + "-]")
        if b1 > b0:
            parts.append("{+" + "".join(new_tokens[b0:b1]).strip() + "+}")
    return "".join(parts)


def compare(old: list[str], new: list[str]) -> list[dict]:
    """Computes block-level changes between two block lists.

    Args:
        old: Blocks of the original document.
        new: Blocks of the updated document.

    Returns:
        Change records with keys `op` (added, removed, changed), 1-based `old_index` and
        `new_index`, the `old` and `new` text, and `diff` (inline diff for `changed`).
    """
    changes: list[dict] = []
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":
            continue
        paired = min(a1 - a0, b1 - b0) if op == "replace" else 0
        for offset in range(paired):
            before, after = old[a0 + offset], new[b0 + offset]
            changes.append(
                {"op": "changed", "old_index": a0 + offset + 1, "new_index": b0 + offset + 1,
                 "old": before, "new": after, "diff": word_diff(before, after)}
            )  # fmt: skip
        for index in range(a0 + paired, a1):
            changes.append({"op": "removed", "old_index": index + 1, "old": old[index]})
        for index in range(b0 + paired, b1):
            changes.append({"op": "added", "new_index": index + 1, "new": new[index]})
    return changes


def render_markdown(old_path: Path, new_path: Path, changes: list[dict]) -> str:
    """Formats changes as a markdown report.

    Args:
        old_path: Path of the original document.
        new_path: Path of the updated document.
        changes: Records returned by `compare`.

    Returns:
        A markdown report with a summary and one bullet per change.
    """
    counts = {op: sum(c["op"] == op for c in changes) for op in ("added", "removed", "changed")}
    lines = [
        f"# Comparison: {old_path.name} -> {new_path.name}",
        "",
        f"Summary: {counts['changed']} changed, {counts['added']} added, "
        f"{counts['removed']} removed.",
        "",
    ]
    if not changes:
        lines.append("No differences found.")
    for change in changes:
        if change["op"] == "changed":
            lines.append(f"- CHANGED (old #{change['old_index']} / new #{change['new_index']}): "
                         f"{change['diff']}")  # fmt: skip
        elif change["op"] == "added":
            lines.append(f"- ADDED (new #{change['new_index']}): {change['new']}")
        else:
            lines.append(f"- REMOVED (old #{change['old_index']}): {change['old']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point.

    Args:
        argv: Argument list; defaults to `sys.argv[1:]`.

    Returns:
        Process exit code (0 on success, 2 when an input file is missing).
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    for path in (args.old, args.new):
        if not path.is_file():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 2
    changes = compare(extract_blocks(args.old), extract_blocks(args.new))
    if args.format == "json":
        print(json.dumps(changes, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(args.old, args.new, changes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
