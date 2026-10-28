from google.adk.events import Event
from google.adk.sessions import Session
from google.genai import types

from coding_agent.config import Settings
from coding_agent.memory import build_memory_service, build_session_service

# ---- Mocks, fixtures & helpers ---- #


def make_session(session_id: str, user_text: str) -> Session:
    event = Event(
        author="user",
        content=types.Content(role="user", parts=[types.Part(text=user_text)]),
    )
    return Session(id=session_id, app_name="app", user_id="u1", events=[event])


async def search(service, query: str, user_id: str = "u1") -> list[str]:
    response = await service.search_memory(app_name="app", user_id=user_id, query=query)
    return [part.text for memory in response.memories for part in memory.content.parts]


# ---- Happy path ---- #


async def test_search_memory_after_saving_session_returns_matching_content(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    service = build_memory_service(settings)
    await service.add_session_to_memory(make_session("s1", "My favourite language is Haskell"))

    results = await search(service, "favourite language")

    assert results == ["My favourite language is Haskell"]


async def test_memory_persists_across_service_instances(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    first = build_memory_service(settings)
    await first.add_session_to_memory(make_session("s1", "Project codename is Falcon"))

    second = build_memory_service(settings)

    assert await search(second, "codename") == ["Project codename is Falcon"]


async def test_session_persists_across_service_instances(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    await build_session_service(settings).create_session(
        app_name="app", user_id="u1", session_id="s1", state={"k": "v"}
    )

    restored = await build_session_service(settings).get_session(
        app_name="app", user_id="u1", session_id="s1"
    )

    assert restored is not None and restored.state == {"k": "v"}


# ---- Error paths ---- #


async def test_search_memory_unrelated_query_returns_nothing(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    service = build_memory_service(settings)
    await service.add_session_to_memory(make_session("s1", "We use PostgreSQL"))

    assert await search(service, "kubernetes") == []


# ---- Edge cases ---- #


async def test_search_memory_other_user_cannot_see_memories(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    service = build_memory_service(settings)
    await service.add_session_to_memory(make_session("s1", "Secret plan alpha"))

    assert await search(service, "secret plan", user_id="u2") == []


async def test_search_memory_punctuation_in_query_does_not_raise(settings: Settings):
    settings.data_dir.mkdir(parents=True)
    service = build_memory_service(settings)
    await service.add_session_to_memory(make_session("s1", "Deploy with docker"))

    assert await search(service, 'what\'s "docker" (AND) deploy?') == ["Deploy with docker"]
