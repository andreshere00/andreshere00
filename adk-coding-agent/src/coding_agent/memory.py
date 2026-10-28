from pathlib import Path

from google.adk.agents.callback_context import CallbackContext
from google.adk.memory import BaseMemoryService, SqliteMemoryService
from google.adk.sessions import BaseSessionService
from google.adk.sessions.sqlite_session_service import SqliteSessionService

from coding_agent.config import Settings


def build_session_service(settings: Settings) -> BaseSessionService:
    """Creates the persistent short-term memory (conversation state) service.

    Args:
        settings: Application settings.

    Returns:
        A SQLite-backed session service stored under `data_dir`.
    """
    return SqliteSessionService(str(Path(settings.data_dir) / "sessions.db"))


def build_memory_service(settings: Settings) -> BaseMemoryService:
    """Creates the persistent long-term memory service with full-text search.

    Args:
        settings: Application settings.

    Returns:
        A SQLite FTS5-backed memory service stored under `data_dir`.
    """
    return SqliteMemoryService(Path(settings.data_dir) / "memory.db")


async def save_session_to_memory(callback_context: CallbackContext) -> None:
    """After-agent callback that ingests the finished turn into long-term memory.

    Args:
        callback_context: ADK callback context for the current invocation.
    """
    await callback_context.add_session_to_memory()
