# Implementation plan: local coding agent on Google ADK

## 1. Goals

A coding agent that runs entirely on the user's machine and has four building blocks:

| Block | Requirement | Realisation |
|---|---|---|
| Filesystem | Read / write / edit files | ADK `EnvironmentToolset` (`ReadFile`, `WriteFile`, `EditFile`, `Execute`) on a workspace-jailed environment |
| Memory | Remember across turns and sessions | ADK `SqliteSessionService` (short-term) + `SqliteMemoryService` with FTS5 (long-term) |
| Sandbox | Run generated code safely | `SandboxEnvironment` with a Docker backend (preferred) and a resource-limited process fallback |
| LLM | OpenRouter | ADK `LiteLlm` with the `openrouter/<model>` route |

Extra requirement: **compare versions of documents**, backed by a **skills repository**, with
support for **Anthropic's `docx` skill**.

## 2. Architecture

```
                        ┌──────────────────────────────┐
   user ── CLI/Runner ─▶│  LlmAgent "coding_agent"      │──▶ OpenRouter (LiteLlm)
                        │  instruction + 4 toolsets     │
                        └──────┬───────┬────────┬───────┘
                               │       │        │
              EnvironmentToolset  SkillToolset  PreloadMemory / load_memory
                               │       │        │
                        ┌──────▼───────▼───┐  ┌─▼─────────────────────┐
                        │ SandboxEnvironment│  │ SqliteMemoryService   │
                        │  files (jailed)   │  │ SqliteSessionService  │
                        │  execute() ───────┼─▶│ (.agent_data/*.db)    │
                        └──────┬────────────┘  └───────────────────────┘
                 DockerSandbox │ ProcessSandbox
                               ▼
                         workspace/  (+ .skills/ materialised on demand)

   SkillRepository ──▶ skills/local/*  (committed, e.g. doc-diff)
                       skills/vendor/* (pinned git sources, e.g. Anthropic docx)
```

### Design decisions

1. **Compose ADK primitives, do not rebuild them.** ADK 2.x already ships the file tools,
   skill toolset, SQLite memory and session services. Custom code is limited to what ADK lacks:
   a *real* sandbox, the skills repository, and wiring.
2. **One environment object is both filesystem and sandbox.** `EnvironmentToolset` and
   `SkillToolset` take the same `SandboxEnvironment`, so a script materialised by a skill sees
   exactly the files the agent wrote.
3. **Workspace jail.** All file tool paths go through `SandboxEnvironment.resolve`, which
   resolves symlinks and rejects anything outside the workspace.
4. **Sandbox backends behind one interface.**
   - `DockerSandbox`: `--network none`, `--cap-drop ALL`, `no-new-privileges`, memory/CPU/PID
     caps, non-root user, workspace bind-mounted at the *same absolute path* (no path
     translation between host and container).
   - `ProcessSandbox`: fallback when Docker is unavailable. Scrubbed environment (API keys are
     not inherited), POSIX rlimits, process-group kill on timeout. **Not an isolation
     boundary**; logs a warning at start-up.
   - `SANDBOX_BACKEND=auto` picks Docker only when the image exists.
5. **Two-tier memory.** Sessions keep conversation state per `session_id`. An
   `after_agent_callback` ingests each finished turn into long-term memory;
   `PreloadMemoryTool` injects relevant past turns automatically and `load_memory` lets the
   model search explicitly. Scope is `(app, user_id)`.
6. **Skills repository with provenance.**
   - `skills/local/`: skills authored here (committed).
   - `skills/vendor/`: third-party skills fetched by `coding-agent skills-sync` from the git
     source and commit pinned in `skills/sources.toml`; resolved commits are recorded in
     `vendor/.lock.json`. Local skills override vendored ones by name.
   - Skills use the open `SKILL.md` format and ADK's progressive disclosure (catalog first,
     instructions and scripts loaded on demand).
7. **Anthropic `docx` skill is fetched, not committed.** Its licence is proprietary
   (governed by Anthropic's terms), so it is pinned by commit and downloaded on the user's
   machine rather than redistributed in this repository.
8. **Document version comparison as a skill.** `doc-diff` ships a stdlib + `python-docx`
   script that extracts headings, paragraphs and table rows from `.docx` (or lines from text
   files), aligns them with `difflib`, and reports added / removed / changed blocks with
   word-level markers (`[-old-]{+new+}`), as markdown or JSON. The skill documents a
   `<name>.v<N>.docx` convention and tells the agent never to overwrite earlier versions.
   Producing tracked-changes output is delegated to the Anthropic `docx` skill.

## 3. Repository layout

```
adk-coding-agent/
├── pyproject.toml
├── .env.example
├── docs/PLAN.md
├── sandbox/Dockerfile            python, pandoc, LibreOffice, poppler, node + docx
├── skills/
│   ├── sources.toml              pinned upstream skills
│   ├── local/doc-diff/           SKILL.md + scripts/diff_docs.py
│   └── vendor/                   (git-ignored) fetched skills
├── src/coding_agent/
│   ├── config.py                 Settings from env / .env
│   ├── sandbox.py                SandboxEnvironment, ProcessSandbox, DockerSandbox
│   ├── memory.py                 session + memory services, save-turn callback
│   ├── skills.py                 SkillRepository (sync, lock, load)
│   ├── agent.py                  build_model, build_agent
│   └── cli.py                    chat, skills-sync, skills-list
└── tests/                        sandbox, skills, memory, diff script, agent e2e
```

## 4. Delivery phases

| # | Phase | Output | Status |
|---|---|---|---|
| 1 | Scaffold, settings, packaging | `pyproject.toml`, `config.py` | done |
| 2 | Filesystem + sandbox | `SandboxEnvironment`, process and Docker backends, image | done (Docker backend not exercised here: no Docker daemon in the build VM) |
| 3 | LLM via OpenRouter | `build_model` (LiteLLM) | done (verified against a local OpenRouter-compatible stub, not the live API) |
| 4 | Memory | session + long-term services, auto-ingest, preload | done |
| 5 | Skills repository + Anthropic docx | `SkillRepository`, `sources.toml`, sync/lock | done |
| 6 | Document comparison | `doc-diff` skill and script | done |
| 7 | Agent assembly + CLI | `build_agent`, `coding-agent chat` | done |
| 8 | Tests | 43 tests (unit + scripted-LLM end-to-end through the real ADK runner) | done |

## 5. Verification strategy

- Unit tests per component (path jail incl. symlink escape, timeouts, secret scrubbing, skill
  sync from a throw-away git repo, memory persistence and user isolation, diff semantics).
- End-to-end tests drive the real ADK `Runner` with a scripted LLM and assert that the
  `doc-diff` skill actually executes inside the sandbox and that memory from session 1 is
  preloaded in session 2.
- Manual: CLI run against a local OpenRouter-compatible stub confirmed routing, model slug,
  bearer auth and sandboxed tool execution.

## 6. Risks and follow-ups

| Risk / gap | Mitigation / next step |
|---|---|
| `ProcessSandbox` is not isolated | Prefer Docker; consider `bubblewrap`/`nsjail` as a third backend |
| Docker backend untested in CI | Add a CI job with Docker that builds the image and runs the sandbox tests |
| Memory is keyword (FTS5) search, not semantic | Swap in an embedding-backed `BaseMemoryService`; only `memory.py` changes |
| Tool output is not stored as memory facts | Add an explicit `remember(fact)` tool writing via `add_memory` |
| `doc-diff` compares accepted-view text only | Extend with formatting diff, or generate redlines via the `docx` skill |
| `EnvironmentToolset` is marked experimental in ADK | Pin `google-adk` minor version when releasing |
| LiteLLM needs `mcp` importable on the async path | Declared as an explicit dependency |
| Human approval for destructive commands | Add ADK tool confirmation for `Execute` when running with `process` backend |
