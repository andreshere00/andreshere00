import asyncio
import logging
import os
import resource
import shutil
import signal
import subprocess
import sys
import uuid
from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path

from google.adk.environment import BaseEnvironment, ExecutionResult

from coding_agent.config import Settings

logger = logging.getLogger(__name__)

MEMORY_LIMIT_BYTES: int = 2 * 1024**3
FILE_SIZE_LIMIT_BYTES: int = 256 * 1024**2
OPEN_FILES_LIMIT: int = 1024
KILL_GRACE_SECONDS: float = 5.0


class SandboxEnvironment(BaseEnvironment):
    """Workspace-jailed filesystem plus sandboxed command execution.

    One object serves as both the agent filesystem and the execution sandbox, so ADK's
    `EnvironmentToolset` and `SkillToolset` share the same view of the workspace. File
    access is confined to `workspace`; subclasses decide how commands are isolated.
    """

    def __init__(self, workspace: Path, timeout: float = 60.0) -> None:
        """Initializes the environment.

        Args:
            workspace: Directory the agent may read, write and execute in.
            timeout: Maximum wall-clock seconds for any command.
        """
        self._workspace = workspace.resolve()
        self._timeout = timeout

    @property
    def working_dir(self) -> Path:
        """Absolute path of the workspace root."""
        return self._workspace

    async def initialize(self) -> None:
        """Creates the workspace directory if needed."""
        self._workspace.mkdir(parents=True, exist_ok=True)
        self._is_initialized = True

    def resolve(self, path: str | Path) -> Path:
        """Resolves a path against the workspace and rejects escapes.

        Args:
            path: Absolute or workspace-relative path.

        Returns:
            The fully resolved absolute path (symlinks followed).

        Raises:
            PermissionError: If the resolved path lies outside the workspace.
        """
        resolved = (self._workspace / path).resolve()
        if not resolved.is_relative_to(self._workspace):
            raise PermissionError(f"Path '{path}' is outside the workspace.")
        return resolved

    async def read_file(self, path: Path) -> bytes:
        """Reads a workspace file.

        Args:
            path: Absolute or workspace-relative path.

        Returns:
            Raw file bytes.

        Raises:
            PermissionError: If the path escapes the workspace.
            FileNotFoundError: If the file does not exist.
        """
        return await asyncio.to_thread(self.resolve(path).read_bytes)

    async def write_file(self, path: Path, content: str | bytes) -> None:
        """Writes a workspace file, creating parent directories.

        Args:
            path: Absolute or workspace-relative path.
            content: Text (UTF-8 encoded) or raw bytes.

        Raises:
            PermissionError: If the path escapes the workspace.
        """
        target = self.resolve(path)
        data = content.encode() if isinstance(content, str) else content

        def _write() -> None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

        await asyncio.to_thread(_write)

    @abstractmethod
    def _launch_spec(self, command: str, run_id: str) -> tuple[list[str], dict[str, str]]:
        """Returns the argv and environment used to run a command."""

    def _preexec(self) -> Callable[[], None] | None:
        """Returns an optional hook executed in the child before `exec`."""
        return None

    async def _on_timeout(self, run_id: str) -> None:
        """Hook for backends needing extra cleanup when a command times out."""

    async def execute(self, command: str, *, timeout: float | None = None) -> ExecutionResult:
        """Runs a shell command inside the sandbox.

        Args:
            command: Shell command line.
            timeout: Per-call limit in seconds, capped by the environment limit.

        Returns:
            Exit code, captured output and whether the command timed out.
        """
        limit = min(timeout or self._timeout, self._timeout)
        run_id = uuid.uuid4().hex[:12]
        argv, env = self._launch_spec(command, run_id)
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self._workspace,
            env=env,
            start_new_session=True,
            preexec_fn=self._preexec(),
        )
        timed_out = False
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=limit)
        except TimeoutError:
            timed_out = True
            await self._on_timeout(run_id)
            _kill_group(proc)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), KILL_GRACE_SECONDS)
        return ExecutionResult(
            exit_code=proc.returncode or 0,
            stdout=stdout.decode(errors="replace"),
            stderr=stderr.decode(errors="replace"),
            timed_out=timed_out,
        )


def _kill_group(proc: asyncio.subprocess.Process) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


class ProcessSandbox(SandboxEnvironment):
    """Best-effort sandbox using a scrubbed subprocess with POSIX resource limits.

    Warning:
        This is NOT an isolation boundary. Commands run as the current user with host
        filesystem and network access. It only strips secrets from the environment and
        bounds CPU time, memory, file size and wall-clock. Use `DockerSandbox` for
        untrusted code.
    """

    def _launch_spec(self, command: str, run_id: str) -> tuple[list[str], dict[str, str]]:
        search_path = f"{Path(sys.executable).parent}:/usr/local/bin:/usr/bin:/bin"
        env = {
            "PATH": search_path,
            "HOME": str(self._workspace),
            "LANG": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        return ["bash", "-c", command], env

    def _preexec(self) -> Callable[[], None]:
        cpu_seconds = int(self._timeout) + 1

        def apply_limits() -> None:
            limits = {
                resource.RLIMIT_CPU: cpu_seconds,
                resource.RLIMIT_AS: MEMORY_LIMIT_BYTES,
                resource.RLIMIT_FSIZE: FILE_SIZE_LIMIT_BYTES,
                resource.RLIMIT_NOFILE: OPEN_FILES_LIMIT,
            }
            for kind, value in limits.items():
                try:
                    resource.setrlimit(kind, (value, value))
                except (ValueError, OSError):
                    pass

        return apply_limits


class DockerSandbox(SandboxEnvironment):
    """Container sandbox: no network, dropped capabilities, bounded memory/CPU/PIDs.

    The workspace is bind-mounted at the same absolute path inside the container, so host
    and container paths are identical and tools need no path translation.
    """

    def __init__(
        self,
        workspace: Path,
        image: str,
        timeout: float = 60.0,
        allow_network: bool = False,
    ) -> None:
        """Initializes the container sandbox.

        Args:
            workspace: Directory mounted read-write into the container.
            image: Docker image providing bash, python and the document tooling.
            timeout: Maximum wall-clock seconds for any command.
            allow_network: Whether the container gets network access.
        """
        super().__init__(workspace, timeout)
        self._image = image
        self._allow_network = allow_network

    def _launch_spec(self, command: str, run_id: str) -> tuple[list[str], dict[str, str]]:
        root = str(self._workspace)
        argv = [
            "docker", "run", "--rm", "--init", "--name", f"agent-sandbox-{run_id}",
            "--network", "bridge" if self._allow_network else "none",
            "--memory", "1g", "--cpus", "1", "--pids-limit", "256",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "-e", f"HOME={root}", "-v", f"{root}:{root}", "-w", root,
            self._image, "bash", "-c", command,
        ]  # fmt: skip
        return argv, {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}

    async def _on_timeout(self, run_id: str) -> None:
        killer = await asyncio.create_subprocess_exec(
            "docker", "kill", f"agent-sandbox-{run_id}",
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
        )  # fmt: skip
        await killer.wait()


def docker_image_available(image: str) -> bool:
    """Checks that the docker CLI exists, the daemon answers and the image is present.

    Args:
        image: Image reference to look up.

    Returns:
        True when containers can be started from the image.
    """
    if shutil.which("docker") is None:
        return False
    probe = subprocess.run(
        ["docker", "image", "inspect", image], capture_output=True, check=False, timeout=15
    )
    return probe.returncode == 0


def create_sandbox(settings: Settings) -> SandboxEnvironment:
    """Creates the sandbox selected by the settings.

    Args:
        settings: Application settings.

    Returns:
        A `DockerSandbox` when requested (or `auto` and available), else a `ProcessSandbox`.

    Raises:
        RuntimeError: If `docker` is requested but unavailable.
    """
    workspace, timeout = settings.workspace_dir, settings.sandbox_timeout
    use_docker = settings.sandbox_backend == "docker" or (
        settings.sandbox_backend == "auto" and docker_image_available(settings.sandbox_image)
    )
    if use_docker:
        if not docker_image_available(settings.sandbox_image):
            raise RuntimeError(
                f"Docker image '{settings.sandbox_image}' not found. "
                "Build it with: docker build -t coding-agent-sandbox sandbox/"
            )
        return DockerSandbox(workspace, settings.sandbox_image, timeout)
    logger.warning("Using ProcessSandbox: commands are NOT isolated from the host.")
    return ProcessSandbox(workspace, timeout)
