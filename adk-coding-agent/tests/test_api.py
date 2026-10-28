import json

import pytest
from fastapi.testclient import TestClient

from coding_agent.api import create_app
from coding_agent.cli import build_runner
from coding_agent.config import Settings
from coding_agent.sandbox import ProcessSandbox
from conftest import make_docx
from test_agent_e2e import ScriptedLlm, call, request_text, say

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


def seed_versions(env: ProcessSandbox) -> None:
    (env.working_dir / "documents").mkdir(exist_ok=True)
    make_docx(env.working_dir / "documents" / "plan.v1.docx", ["Budget is 10 EUR."])
    make_docx(env.working_dir / "documents" / "plan.v2.docx", ["Budget is 20 EUR.", "New risk."])


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


def test_compare_returns_git_style_hunks_with_word_segments_and_stats(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    seed_versions(env)

    body = client.post(
        "/api/compare", json={"old": "documents/plan.v1.docx", "new": "documents/plan.v2.docx"}
    ).json()

    assert body["stats"] == {"changed": 1, "added": 1, "removed": 0}
    deleted = next(
        line for hunk in body["hunks"] for line in hunk["lines"] if line["type"] == "delete"
    )
    assert [(s["kind"], s["text"]) for s in deleted["segments"]] == [
        ("equal", "Budget is "),
        ("delete", "10"),
        ("equal", " EUR."),
    ]


def test_upload_document_stores_valid_docx_under_documents_folder(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    source = make_docx(workspace_settings.workspace_dir / "src.docx", ["hello"])

    response = client.put("/api/documents/My report.docx", content=source.read_bytes())

    assert response.json()["path"] == "documents/My report.docx"
    assert (env.working_dir / "documents" / "My report.docx").exists()
    assert "documents/My report.docx" in [d["path"] for d in client.get("/api/documents").json()]


def test_upload_document_existing_name_is_never_overwritten(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)
    data = make_docx(workspace_settings.workspace_dir / "src.docx", ["hello"]).read_bytes()
    client.put("/api/documents/a.docx", content=data)

    second = client.put("/api/documents/a.docx", content=data).json()

    assert second["path"] == "documents/a-2.docx"


def test_ask_streams_answer_and_puts_documents_in_system_instruction(workspace_settings: Settings):
    env = ProcessSandbox(workspace_settings.workspace_dir, timeout=30)
    llm = ScriptedLlm(script=[say("The budget doubled [2].")])
    runner = build_runner(workspace_settings, model=llm, environment=env)
    client = TestClient(create_app(workspace_settings, runner=runner, environment=env))
    seed_versions(env)

    events = read_events(
        client.post(
            "/api/ask",
            json={
                "old": "documents/plan.v1.docx",
                "new": "documents/plan.v2.docx",
                "question": "What changed in the budget?",
                "session_id": "q1",
            },
        )
    )

    system = str(llm.requests[0].config.system_instruction)
    assert "Budget is 10 EUR." in system and "Budget is 20 EUR." in system
    assert "+Budget is 20 EUR." in system
    assert [e["kind"] for e in events][-2:] == ["message", "done"]
    assert "Budget is 20 EUR." not in request_text(llm.requests[0]).split(system)[-1]


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


def test_upload_document_non_docx_extension_returns_400(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    assert client.put("/api/documents/evil.exe", content=b"MZ").status_code == 400


def test_upload_document_fake_docx_content_returns_400(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    assert client.put("/api/documents/fake.docx", content=b"not a zip").status_code == 400


def test_compare_path_traversal_returns_403(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    response = client.post("/api/compare", json={"old": "../../etc/passwd", "new": "x.docx"})

    assert response.status_code == 403


def test_compare_missing_document_returns_404(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    response = client.post("/api/compare", json={"old": "a.docx", "new": "b.docx"})

    assert response.status_code == 404


def test_compare_corrupt_docx_returns_422(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / "bad.docx").write_bytes(b"not a zip")
    make_docx(env.working_dir / "ok.docx", ["x"])

    assert (
        client.post("/api/compare", json={"old": "bad.docx", "new": "ok.docx"}).status_code == 422
    )


def test_ask_unknown_document_returns_404(workspace_settings: Settings):
    client, _ = make_client(workspace_settings)

    response = client.post("/api/ask", json={"old": "a.docx", "new": "b.docx", "question": "?"})

    assert response.status_code == 404


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


def test_compare_identical_documents_returns_no_hunks(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    make_docx(env.working_dir / "a.docx", ["Same."])
    make_docx(env.working_dir / "b.docx", ["Same."])

    body = client.post("/api/compare", json={"old": "a.docx", "new": "b.docx"}).json()

    assert body["hunks"] == []
    assert body["stats"] == {"changed": 0, "added": 0, "removed": 0}


def test_compare_text_files_are_supported(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    (env.working_dir / "a.txt").write_text("one\ntwo\n")
    (env.working_dir / "b.txt").write_text("one\nthree\n")

    body = client.post("/api/compare", json={"old": "a.txt", "new": "b.txt"}).json()

    assert body["stats"]["changed"] == 1


def test_documents_listing_only_includes_docx_files(workspace_settings: Settings):
    client, env = make_client(workspace_settings)
    make_docx(env.working_dir / "a.docx", ["x"])
    (env.working_dir / "notes.txt").write_text("x")

    assert [d["path"] for d in client.get("/api/documents").json()] == ["a.docx"]
