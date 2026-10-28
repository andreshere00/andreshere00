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

### One command (poe)

```bash
cd adk-coding-agent        # the project lives in this subfolder of the repo
uv sync            # installs the project and the dev group (pytest, ruff, poe)
uv run poe dev     # installs web deps, then runs API (:8000) and Vite (:5173) together; Ctrl+C stops both
poe start   # builds the frontend and serves everything from the API on :8000
```

`poe` alone lists all tasks (`api`, `web`, `web-build`, `test`, `lint`). Open
http://127.0.0.1:5173 with `poe dev` (hot reload, `/api` is proxied to the backend).

### Web UI

```bash
cd web && npm install && npm run build && cd ..   # once
coding-agent serve                                # http://127.0.0.1:8000
```

The UI (React, Vite, Tailwind, [shadcn/ui](https://ui.shadcn.com)) is built around one task:

1. Choose two Word documents from the workspace, or drop/upload `.docx` files (stored in
   `workspace/documents/`).
2. Read a git-style diff (unified or split, with line numbers, `@@` hunks and word-level
   highlights) plus changed/added/removed counts.
3. Ask questions about the content. Both documents and their diff are given to the model as
   context, so it answers from the text and cites block numbers.

Sample documents with several versions (service agreement v1/v2/v3, meeting notes v1/v2, an
identical privacy-policy pair) are created in `workspace/examples/` the first time `serve` finds no
`.docx` files; run `coding-agent seed-examples` to create them at any time. Skills and memory
search are available below. For frontend development run `coding-agent serve`
and `npm run dev` in `web/` (Vite proxies `/api`). The visual style is documented in
[`docs/DESIGN.md`](docs/DESIGN.md). The comparison API is `GET /api/documents`,
`PUT /api/documents/{name}`, `POST /api/compare` and `POST /api/ask` (SSE).

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
