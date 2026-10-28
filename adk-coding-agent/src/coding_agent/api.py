import io
import json
import re
import uuid
import zipfile
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from google.adk.events import Event
from google.adk.runners import Runner
from google.genai import types
from pydantic import BaseModel

from coding_agent.agent import build_agent
from coding_agent.config import APP_NAME, Settings
from coding_agent.docdiff import DOC_CONTEXT_KEY, DocumentComparer
from coding_agent.memory import build_memory_service, build_session_service
from coding_agent.sandbox import SandboxEnvironment, create_sandbox
from coding_agent.skills import SkillRepository

DEFAULT_USER: str = "local"
MAX_FILES: int = 500
MAX_PREVIEW_BYTES: int = 200_000
MAX_PAYLOAD_CHARS: int = 4_000
MAX_UPLOAD_BYTES: int = 20 * 1024 * 1024
UPLOAD_DIR: str = "documents"
HIDDEN_DIRS: frozenset[str] = frozenset({".skills", ".git", "__pycache__", "node_modules", ".tmp"})


class ChatRequest(BaseModel):
    """Body of `POST /api/chat`.

    Attributes:
        session_id: Conversation to continue; a new one is created when omitted.
        message: User message.
    """

    session_id: str | None = None
    message: str


class CompareRequest(BaseModel):
    """Body of `POST /api/compare`.

    Attributes:
        old: Workspace path of the original document.
        new: Workspace path of the revised document.
    """

    old: str
    new: str


class AskRequest(CompareRequest):
    """Body of `POST /api/ask`: a question about a document pair.

    Attributes:
        question: User question.
        session_id: Conversation to continue; a new one is created when omitted.
    """

    question: str
    session_id: str | None = None


def event_to_items(event: Event) -> list[dict[str, Any]]:
    """Converts an ADK event into UI-friendly items.

    Args:
        event: Event emitted by the runner or stored in a session.

    Returns:
        Items of kind `message`, `tool_call` or `tool_result`, in display order.
    """
    items: list[dict[str, Any]] = []
    role = "user" if event.author == "user" else "assistant"
    for part in (event.content.parts if event.content else None) or []:
        if part.text and not part.thought:
            items.append({"kind": "message", "role": role, "text": part.text})
        if part.function_call:
            items.append(
                {"kind": "tool_call", "name": part.function_call.name,
                 "args": _clip(part.function_call.args or {})}
            )  # fmt: skip
        if part.function_response:
            items.append(
                {"kind": "tool_result", "name": part.function_response.name,
                 "response": _clip(part.function_response.response or {})}
            )  # fmt: skip
    return items


def _clip(payload: Any) -> Any:
    """Truncates oversized tool payloads so they stay cheap to send to the browser."""
    text = json.dumps(payload, default=str, ensure_ascii=False)
    if len(text) <= MAX_PAYLOAD_CHARS:
        return json.loads(text)
    return {"truncated": text[:MAX_PAYLOAD_CHARS] + "..."}


def _is_docx(data: bytes) -> bool:
    """Checks that bytes are a zip archive containing a Word document body."""
    if not zipfile.is_zipfile(io.BytesIO(data)):
        return False
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        return "word/document.xml" in archive.namelist()


def _sse(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def create_app(
    settings: Settings,
    runner: Runner | None = None,
    environment: SandboxEnvironment | None = None,
    static_dir: Path | None = None,
) -> FastAPI:
    """Creates the HTTP API (and optionally serves the built web UI).

    Args:
        settings: Application settings.
        runner: Optional pre-built runner, mainly for tests. Otherwise one is created lazily
            on the first chat so the UI can start without an OpenRouter key.
        environment: Optional sandbox override; shared by the runner and the file endpoints.
        static_dir: Directory with the built frontend to serve at `/`.

    Returns:
        The FastAPI application.
    """
    app = FastAPI(title="Coding agent")
    env = environment or create_sandbox(settings)
    repository = SkillRepository(settings.skills_dir)
    sessions = build_session_service(settings)
    memory = build_memory_service(settings)
    comparer = DocumentComparer(repository, env)
    state: dict[str, Runner] = {"runner": runner} if runner else {}

    def get_runner() -> Runner:
        if "runner" not in state:
            state["runner"] = Runner(
                app_name=APP_NAME,
                agent=build_agent(settings, environment=env),
                session_service=sessions,
                memory_service=memory,
                auto_create_session=True,
            )
        return state["runner"]

    def list_files() -> list[dict[str, Any]]:
        root = env.working_dir
        found: list[dict[str, Any]] = []
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if HIDDEN_DIRS.intersection(relative.parts) or not path.is_file():
                continue
            stat = path.stat()
            found.append(
                {"path": relative.as_posix(), "size": stat.st_size, "modified": stat.st_mtime}
            )
        return found[:MAX_FILES]

    @app.get("/api/status")
    async def status() -> dict[str, Any]:
        listed = await sessions.list_sessions(app_name=APP_NAME, user_id=DEFAULT_USER)
        return {
            "model": settings.openrouter_model,
            "llm_configured": bool(settings.openrouter_api_key),
            "sandbox": type(env).__name__.removesuffix("Sandbox").lower(),
            "skills": len(repository.catalog()),
            "files": len(list_files()),
            "sessions": len(listed.sessions),
        }

    @app.get("/api/skills")
    async def skills() -> list[dict[str, str]]:
        return repository.catalog()

    @app.get("/api/files")
    async def files() -> list[dict[str, Any]]:
        return list_files()

    @app.get("/api/files/content")
    async def file_content(path: str) -> dict[str, Any]:
        try:
            target = env.resolve(path)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        if not target.is_file():
            raise HTTPException(status_code=404, detail="File not found.")
        data = target.read_bytes()[:MAX_PREVIEW_BYTES]
        try:
            return {"path": path, "size": target.stat().st_size, "text": data.decode()}
        except UnicodeDecodeError:
            return {"path": path, "size": target.stat().st_size, "text": None}

    @app.get("/api/memory")
    async def search_memory(query: str) -> list[dict[str, Any]]:
        found = await memory.search_memory(app_name=APP_NAME, user_id=DEFAULT_USER, query=query)
        return [
            {
                "author": entry.author,
                "timestamp": entry.timestamp,
                "text": "".join(part.text or "" for part in entry.content.parts or []),
            }
            for entry in found.memories
        ]

    @app.get("/api/sessions")
    async def list_sessions() -> list[dict[str, Any]]:
        listed = await sessions.list_sessions(app_name=APP_NAME, user_id=DEFAULT_USER)
        ordered = sorted(listed.sessions, key=lambda s: s.last_update_time, reverse=True)
        return [{"id": s.id, "updated": s.last_update_time} for s in ordered]

    @app.get("/api/sessions/{session_id}")
    async def session_history(session_id: str) -> list[dict[str, Any]]:
        session = await sessions.get_session(
            app_name=APP_NAME, user_id=DEFAULT_USER, session_id=session_id
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found.")
        return [item for event in session.events for item in event_to_items(event)]

    async def stream_turn(session_id: str, text: str) -> AsyncIterator[str]:
        yield _sse({"kind": "session", "session_id": session_id})
        try:
            message = types.Content(role="user", parts=[types.Part(text=text)])
            async for event in get_runner().run_async(
                user_id=DEFAULT_USER, session_id=session_id, new_message=message
            ):
                for item in event_to_items(event):
                    yield _sse(item)
        except Exception as error:  # surfaced to the UI instead of dropping the stream
            yield _sse({"kind": "error", "text": f"{type(error).__name__}: {error}"})
        yield _sse({"kind": "done"})

    @app.post("/api/chat")
    async def chat(request: ChatRequest) -> StreamingResponse:
        session_id = request.session_id or uuid.uuid4().hex[:8]
        return StreamingResponse(
            stream_turn(session_id, request.message), media_type="text/event-stream"
        )

    @app.get("/api/documents")
    async def documents() -> list[dict[str, Any]]:
        return [f for f in list_files() if f["path"].lower().endswith(".docx")]

    @app.put("/api/documents/{name}")
    async def upload_document(name: str, request: Request) -> dict[str, Any]:
        declared = int(request.headers.get("content-length") or 0)
        if declared > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="File is larger than 20 MB.")
        data = await request.body()
        safe = re.sub(r"[^\w.\- ]", "_", Path(name).name)
        if not safe.lower().endswith(".docx"):
            raise HTTPException(status_code=400, detail="Only .docx files are supported.")
        if len(data) > MAX_UPLOAD_BYTES or not _is_docx(data):
            raise HTTPException(status_code=400, detail="Not a valid Word (.docx) file.")
        target = env.resolve(f"{UPLOAD_DIR}/{safe}")
        counter = 2
        while target.exists():
            target = env.resolve(f"{UPLOAD_DIR}/{Path(safe).stem}-{counter}.docx")
            counter += 1
        await env.write_file(target, data)
        return {"path": target.relative_to(env.working_dir).as_posix(), "size": len(data)}

    @app.post("/api/compare")
    async def compare(request: CompareRequest) -> dict[str, Any]:
        try:
            return comparer.compare(request.old, request.new)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except Exception as error:  # corrupt documents surface as a readable 422
            raise HTTPException(
                status_code=422, detail=f"Cannot read documents: {error}"
            ) from error

    @app.post("/api/ask")
    async def ask(request: AskRequest) -> StreamingResponse:
        session_id = request.session_id or uuid.uuid4().hex[:8]
        try:
            context = comparer.build_context(request.old, request.new)
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except Exception as error:
            raise HTTPException(
                status_code=422, detail=f"Cannot read documents: {error}"
            ) from error
        existing = await sessions.get_session(
            app_name=APP_NAME, user_id=DEFAULT_USER, session_id=session_id
        )
        if existing is None:
            await sessions.create_session(
                app_name=APP_NAME,
                user_id=DEFAULT_USER,
                session_id=session_id,
                state={DOC_CONTEXT_KEY: context},
            )
        return StreamingResponse(
            stream_turn(session_id, request.question), media_type="text/event-stream"
        )

    if static_dir and static_dir.is_dir():
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="web")
    return app
