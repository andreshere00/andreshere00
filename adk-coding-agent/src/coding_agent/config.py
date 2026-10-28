import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

SandboxBackendName = Literal["auto", "docker", "process"]

DEFAULT_MODEL: str = "anthropic/claude-sonnet-4.5"
APP_NAME: str = "coding_agent"


@dataclass(frozen=True)
class Settings:
    """Runtime configuration resolved from environment variables.

    Attributes:
        openrouter_api_key: OpenRouter API key.
        openrouter_model: OpenRouter model slug, e.g. `anthropic/claude-sonnet-4.5`.
        workspace_dir: Directory the agent can read, write and execute in.
        data_dir: Directory holding the session and memory SQLite databases.
        skills_dir: Directory of the skills repository.
        sandbox_backend: `docker`, `process` or `auto` (docker when available).
        sandbox_image: Docker image used by the docker backend.
        sandbox_timeout: Wall-clock limit in seconds for each sandboxed command.
    """

    openrouter_api_key: str
    openrouter_model: str
    workspace_dir: Path
    data_dir: Path
    skills_dir: Path
    sandbox_backend: SandboxBackendName
    sandbox_image: str
    sandbox_timeout: int

    @property
    def litellm_model(self) -> str:
        """Model string in the format LiteLLM uses to route through OpenRouter."""
        return f"openrouter/{self.openrouter_model}"

    @classmethod
    def from_env(cls) -> "Settings":
        """Builds settings from the process environment and an optional `.env` file.

        Returns:
            The resolved settings. Directories are created and made absolute.
        """
        load_dotenv()
        env = os.environ.get
        settings = cls(
            openrouter_api_key=env("OPENROUTER_API_KEY", ""),
            openrouter_model=env("OPENROUTER_MODEL", DEFAULT_MODEL),
            workspace_dir=Path(env("WORKSPACE_DIR", "./workspace")).resolve(),
            data_dir=Path(env("DATA_DIR", "./.agent_data")).resolve(),
            skills_dir=Path(env("SKILLS_DIR", "./skills")).resolve(),
            sandbox_backend=env("SANDBOX_BACKEND", "auto"),  # type: ignore[arg-type]
            sandbox_image=env("SANDBOX_IMAGE", "coding-agent-sandbox:latest"),
            sandbox_timeout=int(env("SANDBOX_TIMEOUT_SECONDS", "60")),
        )
        for directory in (settings.workspace_dir, settings.data_dir):
            directory.mkdir(parents=True, exist_ok=True)
        return settings
