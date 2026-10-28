# ADK coding agent

A local coding agent built on [Google ADK](https://google.github.io/adk-docs/) with a
workspace-jailed filesystem, persistent memory, a sandbox for code execution, an
[OpenRouter](https://openrouter.ai) LLM, and a skills repository (including Anthropic's `docx`
skill and a document version-diff skill).

See [`docs/PLAN.md`](docs/PLAN.md) for the design and rationale.

## Quick start

```bash
cd adk-coding-agent
uv venv && uv pip install -e ".[dev]"      # or: python -m venv .venv && pip install -e ".[dev]"
cp .env.example .env                       # set OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)

coding-agent skills-sync                   # fetch Anthropic's docx skill (pinned commit)
coding-agent skills-list
coding-agent chat                          # interactive
coding-agent chat --prompt "Write fizzbuzz in fizz.py and run it" --session demo
```

State lives in `.agent_data/` (sessions, long-term memory) and files in `workspace/`.

## Sandbox

```bash
docker build -t coding-agent-sandbox sandbox/    # recommended
```

`SANDBOX_BACKEND=auto` uses Docker when the image exists, otherwise falls back to a
resource-limited subprocess that is **not** isolated from your machine (a warning is logged).
Set `SANDBOX_BACKEND=docker` to refuse the fallback.

## Comparing document versions

Put versions in `workspace/` (`contract.v1.docx`, `contract.v2.docx`) and ask:

> What changed between contract.v1.docx and contract.v2.docx?

The agent loads the `doc-diff` skill and runs it in the sandbox. Use the `docx` skill to create
or edit Word files (new versions are saved as new files, never overwriting old ones).

## Skills repository

- `skills/local/`: skills authored in this repo.
- `skills/vendor/`: fetched from the pinned sources in `skills/sources.toml`
  (git-ignored; Anthropic's `docx` skill is proprietary and is not redistributed here).

To add a skill, create `skills/local/<name>/SKILL.md` (name + description frontmatter) with an
optional `scripts/` folder, or add a source to `sources.toml` and run `coding-agent skills-sync`.

## Tests

```bash
pytest
ruff check src tests skills/local
```
