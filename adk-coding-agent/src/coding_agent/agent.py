from google.adk.agents import LlmAgent
from google.adk.models import BaseLlm
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.environment import EnvironmentToolset
from google.adk.tools.load_memory_tool import load_memory_tool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.tools.skill_toolset import SkillToolset

from coding_agent.config import APP_NAME, Settings
from coding_agent.memory import save_session_to_memory
from coding_agent.sandbox import SandboxEnvironment, create_sandbox
from coding_agent.skills import SkillRepository

SKILLS_MOUNT: str = ".skills"

INSTRUCTION: str = """\
You are a careful local coding agent working inside a sandboxed workspace.

- Use ReadFile / EditFile / WriteFile for files and Execute for running programs and tests.
- All paths live inside the workspace. Never try to access anything outside of it.
- Before working on a document task, check the available skills and load the relevant one
  (for example `docx` to create or edit Word files, `doc-diff` to compare document versions).
- Never overwrite an older version of a document; save edits as a new version file.
- Relevant long-term memories are preloaded for you. Use `load_memory` to search for more
  when the user refers to earlier work or preferences.
- Verify your work by running it, then summarise what you changed and what you observed.
"""


def build_model(settings: Settings) -> LiteLlm:
    """Creates the OpenRouter-backed LLM.

    Args:
        settings: Application settings.

    Returns:
        A LiteLLM wrapper routed through OpenRouter.

    Raises:
        ValueError: If no OpenRouter API key is configured.
    """
    if not settings.openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY is not set.")
    return LiteLlm(model=settings.litellm_model, api_key=settings.openrouter_api_key)


def build_agent(
    settings: Settings,
    model: BaseLlm | None = None,
    environment: SandboxEnvironment | None = None,
) -> LlmAgent:
    """Assembles the coding agent from its four building blocks.

    Filesystem and sandbox come from one `SandboxEnvironment`, skills from the
    `SkillRepository`, memory from the SQLite memory service (wired by the runner), and the
    LLM from OpenRouter.

    Args:
        settings: Application settings.
        model: Optional LLM override, mainly for tests.
        environment: Optional environment override, mainly for tests.

    Returns:
        The configured ADK agent.
    """
    env = environment or create_sandbox(settings)
    skills = SkillRepository(settings.skills_dir).load_all()
    return LlmAgent(
        name=APP_NAME,
        model=model or build_model(settings),
        instruction=INSTRUCTION,
        tools=[
            EnvironmentToolset(environment=env),
            SkillToolset(
                skills=skills,
                environment=env,
                skills_folder=env.working_dir / SKILLS_MOUNT,
            ),
            PreloadMemoryTool(),
            load_memory_tool,
        ],
        after_agent_callback=save_session_to_memory,
    )
