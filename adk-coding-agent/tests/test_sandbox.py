from pathlib import Path

import pytest

from coding_agent.config import Settings
from coding_agent.sandbox import DockerSandbox, ProcessSandbox, create_sandbox

# ---- Mocks, fixtures & helpers ---- #


@pytest.fixture
def sandbox(tmp_path: Path) -> ProcessSandbox:
    return ProcessSandbox(tmp_path / "ws", timeout=2)


# ---- Happy path ---- #


async def test_write_file_relative_path_creates_file_inside_workspace(sandbox: ProcessSandbox):
    await sandbox.initialize()

    await sandbox.write_file(Path("src/app.py"), "print('hi')")

    assert (sandbox.working_dir / "src" / "app.py").read_text() == "print('hi')"
    assert await sandbox.read_file(Path("src/app.py")) == b"print('hi')"


async def test_execute_python_script_returns_stdout_and_zero_exit(sandbox: ProcessSandbox):
    await sandbox.initialize()
    await sandbox.write_file(Path("hello.py"), "print('hello sandbox')")

    result = await sandbox.execute("python hello.py")

    assert result.exit_code == 0
    assert result.stdout.strip() == "hello sandbox"
    assert not result.timed_out


async def test_execute_command_runs_with_workspace_as_cwd(sandbox: ProcessSandbox):
    await sandbox.initialize()

    result = await sandbox.execute("pwd")

    assert result.stdout.strip() == str(sandbox.working_dir)


def test_create_sandbox_process_backend_returns_process_sandbox(settings: Settings):
    assert isinstance(create_sandbox(settings), ProcessSandbox)


# ---- Error paths ---- #


async def test_execute_failing_command_returns_exit_code_and_stderr(sandbox: ProcessSandbox):
    await sandbox.initialize()

    result = await sandbox.execute("echo boom >&2; exit 3")

    assert result.exit_code == 3
    assert "boom" in result.stderr


async def test_execute_long_running_command_times_out_and_is_killed(sandbox: ProcessSandbox):
    await sandbox.initialize()

    result = await sandbox.execute("sleep 30", timeout=0.5)

    assert result.timed_out


async def test_read_file_path_outside_workspace_raises_permission_error(sandbox: ProcessSandbox):
    await sandbox.initialize()

    with pytest.raises(PermissionError):
        await sandbox.read_file(Path("../../etc/passwd"))


async def test_write_file_symlink_escaping_workspace_raises_permission_error(
    sandbox: ProcessSandbox, tmp_path: Path
):
    await sandbox.initialize()
    outside = tmp_path / "outside"
    outside.mkdir()
    (sandbox.working_dir / "link").symlink_to(outside)

    with pytest.raises(PermissionError):
        await sandbox.write_file(Path("link/evil.txt"), "x")

    assert not (outside / "evil.txt").exists()


def test_create_sandbox_docker_requested_without_image_raises_runtime_error(settings: Settings):
    docker_settings = Settings(**{**settings.__dict__, "sandbox_backend": "docker"})

    with pytest.raises(RuntimeError, match="not found"):
        create_sandbox(docker_settings)


# ---- Edge cases ---- #


async def test_execute_secrets_in_host_environment_are_not_visible(
    sandbox: ProcessSandbox, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("OPENROUTER_API_KEY", "super-secret")
    await sandbox.initialize()

    result = await sandbox.execute("env")

    assert "super-secret" not in result.stdout


async def test_execute_timeout_argument_is_capped_by_environment_limit(sandbox: ProcessSandbox):
    await sandbox.initialize()

    result = await sandbox.execute("sleep 30", timeout=600)

    assert result.timed_out


def test_docker_sandbox_launch_spec_disables_network_by_default(tmp_path: Path):
    docker = DockerSandbox(tmp_path, image="img")

    argv, _ = docker._launch_spec("ls", "abc")

    assert argv[argv.index("--network") + 1] == "none"
    assert "agent-sandbox-abc" in argv
    assert argv[-3:] == ["bash", "-c", "ls"]
