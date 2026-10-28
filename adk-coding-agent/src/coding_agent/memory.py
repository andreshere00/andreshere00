import logging
from pathlib import Path

from google.adk.agents.callback_context import CallbackContext
from google.adk.memory import BaseMemoryService, SqliteMemoryService
from google.adk.models.llm_request import LlmRequest
from google.adk.sessions import BaseSessionService
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.tools.tool_context import ToolContext
from google.adk.utils.content_utils import extract_text_from_content

from coding_agent.config import Settings

logger = logging.getLogger(__name__)


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


class InstructionMemoryTool(PreloadMemoryTool):
    """Preloads relevant memories into the system instruction instead of a user turn.

    ADK's default tool appends a synthetic user message after the tool results of every model
    call, which can make models stop or repeat tool calls. Using the system instruction keeps
    the conversation structure intact.
    """

    async def process_llm_request(
        self, *, tool_context: ToolContext, llm_request: LlmRequest
    ) -> None:
        """Adds memories matching the user's message to the system instruction.

        Args:
            tool_context: Context carrying the user message and the memory service.
            llm_request: Request about to be sent to the model.
        """
        query = extract_text_from_content(tool_context.user_content, splitter=" ")
        if not query:
            return
        try:
            found = await tool_context.search_memory(query)
        except Exception:
            logger.warning("Failed to preload memory.", exc_info=True)
            return
        lines = [
            f"{entry.author or 'unknown'}: {part.text}"
            for entry in found.memories
            for part in entry.content.parts or []
            if part.text
        ]
        if lines:
            llm_request.append_instructions(
                [
                    "Notes from previous conversations with this user, possibly useful:\n"
                    "<PAST_CONVERSATIONS>\n" + "\n".join(lines) + "\n</PAST_CONVERSATIONS>"
                ]
            )
