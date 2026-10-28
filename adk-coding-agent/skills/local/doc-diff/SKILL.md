---
name: doc-diff
description: Compare two versions of a document (.docx or text) and report what was added, removed or changed, with word-level detail. Use when the user asks what changed between versions, wants a changelog or redline summary, or needs to review revisions of a Word document.
---

# Document version comparison

Use this skill whenever two versions of the same document must be compared.

## Convention for versions

Keep every version as a separate file in the workspace and never overwrite an older one.
Prefer `<name>.v<N>.docx` (for example `contract.v1.docx`, `contract.v2.docx`). When the user
edits a document, save the result as the next version instead of modifying the original.

## Compare two versions

Call `run_skill_script` with `skill_name="doc-diff"`, `file_path="scripts/diff_docs.py"` and a
`command` such as:

```bash
python .skills/doc-diff/scripts/diff_docs.py contract.v1.docx contract.v2.docx
python .skills/doc-diff/scripts/diff_docs.py contract.v1.docx contract.v2.docx --format json
```

Add `--format unified` for git-style hunks (`@@ -a,b +c,d @@`, lines prefixed with space, `-`
or `+`). Paths are relative to the workspace root.

## Reading the output

- `CHANGED`: a paragraph or table row exists in both versions; `[-removed-]` and `{+added+}`
  mark word-level edits.
- `ADDED` / `REMOVED`: a block exists in only one version.
- `#N` is the 1-based block index (paragraph or table row) in the old or new file.
- Headings are shown with a markdown `#` prefix; table rows as `| a | b |`.

## Notes

- Text inside tracked insertions counts as present; tracked deletions are ignored, so each file
  is compared in its "accepted changes" view.
- Formatting-only changes (fonts, spacing) are not reported.
- To produce a Word file with tracked changes from the comparison, use the `docx` skill.
- Summarise the diff for the user in plain language; quote exact text for important changes.
