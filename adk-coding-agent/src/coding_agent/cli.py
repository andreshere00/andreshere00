import argparse
import asyncio
import uuid

from google.adk.runners import Runner
from google.genai import types

from coding_agent.agent import build_agent
from coding_agent.config import APP_NAME, Settings
from coding_agent.memory import build_memory_service, build_session_service
from coding_agent.skills import SkillRepository

DEFAULT_USER: str = "local"


def build_runner(settings: Settings, **agent_overrides) -> Runner:
    """Creates a runner with persistent sessions and long-term memory.

    Args:
        settings: Application settings.
        **agent_overrides: Forwarded to `build_agent` (model, environment).

    Returns:
        A runner that auto-creates sessions on first use.
    """
    return Runner(
        app_name=APP_NAME,
        agent=build_agent(settings, **agent_overrides),
        session_service=build_session_service(settings),
        memory_service=build_memory_service(settings),
        auto_create_session=True,
    )


async def ask(runner: Runner, user_id: str, session_id: str, prompt: str) -> str:
    """Sends one user message and returns the agent's final answer.

    Args:
        runner: Runner created by `build_runner`.
        user_id: User scope for sessions and memory.
        session_id: Conversation to continue.
        prompt: User message.

    Returns:
        The final text response. Tool calls are echoed to stdout as they happen.
    """
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    answer = ""
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        for call in event.get_function_calls():
            print(f"  [tool] {call.name}({dict(call.args or {})})")
        if event.is_final_response() and event.content and event.content.parts:
            answer = "".join(part.text or "" for part in event.content.parts)
    return answer


async def chat(settings: Settings, session_id: str, prompt: str | None) -> None:
    """Runs one prompt, or an interactive loop when no prompt is given.

    Args:
        settings: Application settings.
        session_id: Conversation to create or resume.
        prompt: Optional single message; when set the program exits after answering.
    """
    runner = build_runner(settings)
    if prompt:
        print(await ask(runner, DEFAULT_USER, session_id, prompt))
        return
    print(f"Session {session_id}. Type 'exit' to quit.")
    while (line := input("you> ").strip()) not in {"exit", "quit"}:
        if line:
            print(f"agent> {await ask(runner, DEFAULT_USER, session_id, line)}")


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point.

    Args:
        argv: Argument list; defaults to `sys.argv[1:]`.
    """
    parser = argparse.ArgumentParser(prog="coding-agent")
    commands = parser.add_subparsers(dest="command", required=True)
    chat_parser = commands.add_parser("chat", help="Talk to the agent.")
    chat_parser.add_argument("--session", default=None, help="Session id to resume.")
    chat_parser.add_argument("--prompt", default=None, help="Run a single prompt and exit.")
    commands.add_parser("skills-sync", help="Fetch pinned third-party skills.")
    commands.add_parser("skills-list", help="List available skills.")
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    repository = SkillRepository(settings.skills_dir)
    if args.command == "skills-sync":
        for name, commit in repository.sync().items():
            print(f"{name} @ {commit}")
    elif args.command == "skills-list":
        for skill in repository.load_all():
            print(f"{skill.name}: {skill.frontmatter.description[:90]}")
    else:
        asyncio.run(chat(settings, args.session or uuid.uuid4().hex[:8], args.prompt))
