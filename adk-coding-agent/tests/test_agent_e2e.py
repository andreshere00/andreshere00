from collections.abc import AsyncGenerator

import pytest
from google.adk.models import BaseLlm, LlmRequest, LlmResponse
from google.genai import types

from coding_agent.agent import build_model
from coding_agent.cli import ask, build_runner
from coding_agent.config import Settings
from coding_agent.sandbox import ProcessSandbox
from conftest import make_docx

# ---- Mocks, fixtures & helpers ---- #


def call(name: str, **args) -> LlmResponse:
    part = types.Part(function_call=types.FunctionCall(name=name, args=args))
    return LlmResponse(content=types.Content(role="model", parts=[part]))


def say(text: str) -> LlmResponse:
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))


class ScriptedLlm(BaseLlm):
    """Replays canned responses and records every request it receives."""

    model: str = "scripted"
    script: list[LlmResponse]
    requests: list[LlmRequest] = []

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        self.requests.append(llm_request)
        yield self.script.pop(0)


def function_responses(llm: ScriptedLlm) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for content in llm.requests[-1].contents:
        for part in content.parts or []:
            if part.function_response:
                found[part.function_response.name] = part.function_response.response
    return found


def request_text(request: LlmRequest) -> str:
    texts = [part.text or "" for content in request.contents for part in content.parts or []]
    return "\n".join([str(request.config.system_instruction), *texts])


# ---- Happy path ---- #


async def test_ask_compare_two_docx_versions_runs_doc_diff_skill_in_sandbox(settings: Settings):
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    await env.initialize()
    make_docx(settings.workspace_dir / "plan.v1.docx", ["Budget is 10 EUR."])
    make_docx(settings.workspace_dir / "plan.v2.docx", ["Budget is 20 EUR.", "New risk added."])
    command = "python .skills/doc-diff/scripts/diff_docs.py plan.v1.docx plan.v2.docx"
    llm = ScriptedLlm(
        script=[
            call("load_skill", skill_name="doc-diff"),
            call("run_skill_script", skill_name="doc-diff",
                 file_path="scripts/diff_docs.py", command=command),
            say("Budget changed from 10 to 20 EUR and a risk was added."),
        ]
    )  # fmt: skip
    runner = build_runner(settings, model=llm, environment=env)

    answer = await ask(runner, "u1", "s1", "What changed between plan v1 and v2?")

    script_result = function_responses(llm)["run_skill_script"]
    assert script_result["exit_code"] == 0
    assert "[-10-]{+20+}" in script_result["stdout"]
    assert "ADDED" in script_result["stdout"]
    assert answer.startswith("Budget changed")


async def test_ask_write_and_execute_tools_operate_on_the_workspace(settings: Settings):
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    llm = ScriptedLlm(
        script=[
            call("WriteFile", path="hello.py", content="print(6 * 7)"),
            call("Execute", command="python hello.py"),
            say("It prints 42."),
        ]
    )
    runner = build_runner(settings, model=llm, environment=env)

    await ask(runner, "u1", "s1", "Write and run a script that prints 6*7")

    assert (settings.workspace_dir / "hello.py").read_text() == "print(6 * 7)"
    assert function_responses(llm)["Execute"]["stdout"].strip() == "42"


async def test_ask_second_session_receives_memories_from_the_first(settings: Settings):
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    first = ScriptedLlm(script=[say("Noted.")])
    await ask(build_runner(settings, model=first, environment=env), "u1", "s1",
              "Remember that our staging cluster is called Orion")  # fmt: skip
    second = ScriptedLlm(script=[say("Orion.")])

    await ask(build_runner(settings, model=second, environment=env), "u1", "s2",
              "What is the name of our staging cluster?")  # fmt: skip

    assert "Orion" in request_text(second.requests[0])


# ---- Error paths ---- #


async def test_ask_read_file_outside_workspace_is_rejected(settings: Settings):
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    llm = ScriptedLlm(script=[call("ReadFile", path="/etc/passwd"), say("Blocked.")])
    runner = build_runner(settings, model=llm, environment=env)

    await ask(runner, "u1", "s1", "Read /etc/passwd")

    result = function_responses(llm)["ReadFile"]
    assert result["status"] == "error"


def test_build_model_valid_settings_routes_through_openrouter(settings: Settings):
    assert build_model(settings).model == "openrouter/test/model"


def test_build_runner_without_api_key_raises_value_error(settings: Settings):
    keyless = Settings(**{**settings.__dict__, "openrouter_api_key": ""})

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        build_runner(keyless)


# ---- Edge cases ---- #


async def test_ask_agent_exposes_filesystem_skill_and_memory_tools(settings: Settings):
    env = ProcessSandbox(settings.workspace_dir, timeout=30)
    llm = ScriptedLlm(script=[say("ok")])

    await ask(build_runner(settings, model=llm, environment=env), "u1", "s1", "hi")

    tool_names = set(llm.requests[0].tools_dict)
    assert {"Execute", "ReadFile", "EditFile", "WriteFile", "load_skill", "run_skill_script",
            "load_memory"} <= tool_names  # fmt: skip
