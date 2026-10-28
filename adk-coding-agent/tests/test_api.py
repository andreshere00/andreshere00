import json

import pytest
from fastapi.testclient import TestClient

from coding_agent.api import create_app
from coding_agent.cli import build_runner
from coding_agent.config import Settings
from coding_agent.sandbox import ProcessSandbox
from test_agent_e2e import ScriptedLlm, call, say

# ---- Mocks, fixtures & helpers ---- #


def make_client(
    settings: Settings, script: list | None = None
) -> tuple[TestClient, ProcessSandbox]:
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    runner = None
    if script is not None:
        runner = build_runner(settings, model=ScriptedLlm(script=script), environment=env)
    return TestClient(create_app(settings, runner=runner, environment=env)), env


def read_events(response) -> list[dict]:
    lines = [line for line in response.text.splitlines() if line.startswith("data: ")]
    return [json.loads(line.removeprefix("data: ")) for line in lines]


@pytest.fixture
def workspace_settings(settings: Settings) -> Settings:
    settings.workspace_dir.mkdir(parents=True)
    settings.data_dir.mkdir(parents=True)
    return settings


# ---- Happy path ---- #


def test_chat_streams_tool_call_result_and_final_message(workspace_settings: Settings):
    client, _ = make_client(
        workspace_settings,
        [call("Execute", command="echo hi"), say("All done.")],
    )

    events = read_events(client.post("/api/chat", json={"session_id": "s1", "message": "go"}))

    assert [e["kind"] for e in events] == [
        "session", "tool_call", "tool_result", "message", "done",
    ]  # fmt: skip
    assert events[2]["response"]["stdout"].strip() == "hi"
    assert events[3] == {"kind": "message", "role": "assistant", "text": "All done."}


def test_session_history_replays_user_and_assistant_messages(workspace_settings: Settings):
    client, _ = make_client(workspace_settings, [say("Hello!")])
    client.post("/api/chat", json={"session_id": "s1", "message": "hi there"})

    history = client.get("/api/sessions/s1").json()

    assert [(i["role"], i["text"]) for i in history] == [
        ("user", "hi there"),
        ("assistant", "Hello!"),
    ]
    assert [s["id"] for s in client.get("/api/sessions").json()] == ["s1"]


def test_status_reports_sandbox_skills_and_counts(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / "a.txt").write_text("x")

    status = client.get("/api/status").json()

    assert status["sandbox"] == "process"
    assert status["files"] == 1
    assert status["skills"] >= 1
    assert status["llm_configured"] is True


def test_skills_lists_doc_diff_as_local(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    skills = {s["name"]: s for s in client.get("/api/skills").json()}

    assert skills["doc-diff"]["source"] == "local"


def test_files_content_returns_text_of_workspace_file(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / "notes.md").write_text("# hello")

    body = client.get("/api/files/content", params={"path": "notes.md"}).json()

    assert body["text"] == "# hello"


def test_memory_search_returns_text_saved_by_previous_chat(workspace_settings: Settings):
    client, _ = make_client(workspace_settings, [say("Noted.")])
    client.post("/api/chat", json={"session_id": "s1", "message": "Our staging cluster is Orion"})

    found = client.get("/api/memory", params={"query": "staging cluster"}).json()

    assert any("Orion" in entry["text"] for entry in found)


# ---- Error paths ---- #


def test_chat_without_api_key_streams_error_event(workspace_settings: Settings):
    keyless = Settings(**{**workspace_settings.__dict__, "openrouter_api_key": ""})
    client, _ = make_client(keyless)

    events = read_events(client.post("/api/chat", json={"message": "hi"}))

    assert [e["kind"] for e in events] == ["session", "error", "done"]
    assert "OPENROUTER_API_KEY" in events[1]["text"]


def test_files_content_path_traversal_returns_403(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    response = client.get("/api/files/content", params={"path": "../../etc/passwd"})

    assert response.status_code == 403


def test_files_content_missing_file_returns_404(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    assert client.get("/api/files/content", params={"path": "nope.txt"}).status_code == 404


def test_session_history_unknown_session_returns_404(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    assert client.get("/api/sessions/missing").status_code == 404


# ---- Edge cases ---- #


def test_files_listing_hides_materialised_skills_folder(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / ".skills" / "x").mkdir(parents=True)
    (env.working_dir / ".skills" / "x" / "SKILL.md").write_text("x")
    (env.working_dir / "keep.py").write_text("print(1)")

    assert [f["path"] for f in client.get("/api/files").json()] == ["keep.py"]


def test_files_content_binary_file_returns_null_text(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / "blob.bin").write_bytes(bytes([0xFF, 0xFE, 0x00, 0x80]))

    assert client.get("/api/files/content", params={"path": "blob.bin"}).json()["text"] is None


def test_chat_oversized_tool_output_is_truncated(workspace_settings: Settings):
    client, _ = make_client(
        workspace_settings,
        [call("Execute", command="python -c \"print('x' * 20000)\""), say("ok")],
    )

    events = read_events(client.post("/api/chat", json={"message": "spam"}))

    result = next(e for e in events if e["kind"] == "tool_result")
    assert list(result["response"]) == ["truncated"]
    assert len(result["response"]["truncated"]) < 4100
