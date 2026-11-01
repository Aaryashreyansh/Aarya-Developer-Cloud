from fastapi.testclient import TestClient

from app.main import app
from app.ai import routes

client = TestClient(app)


def test_provider_list_does_not_expose_secrets() -> None:
    response = client.get("/api/v1/providers")
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["providers"]}
    assert ids == {"openai", "gemini", "claude", "openrouter"}
    assert "api_key" not in response.text.lower()


def test_chat_validates_provider() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"provider": "unknown", "prompt": "Hello"},
    )
    assert response.status_code == 422


def test_chat_requires_server_authentication(monkeypatch) -> None:
    monkeypatch.setenv("APP_API_TOKEN", "test-token")
    response = client.post(
        "/api/v1/chat",
        json={"provider": "gemini", "prompt": "Hello"},
    )
    assert response.status_code == 401


def test_chat_uses_provider_adapter(monkeypatch) -> None:
    monkeypatch.setenv("APP_API_TOKEN", "test-token")

    async def fake_generate(provider, prompt, **kwargs):
        return f"reply from {provider}: {prompt}"

    monkeypatch.setattr(routes, "generate", fake_generate)
    response = client.post(
        "/api/v1/chat",
        headers={"X-API-Token": "test-token"},
        json={"provider": "gemini", "prompt": "Write a test"},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "reply from gemini: Write a test"


def test_chat_reports_missing_server_key(monkeypatch) -> None:
    from app.ai.providers import ProviderConfigurationError

    monkeypatch.setenv("APP_API_TOKEN", "test-token")

    async def missing_key(*args, **kwargs):
        raise ProviderConfigurationError("GEMINI_API_KEY is not configured on the server.")

    monkeypatch.setattr(routes, "generate", missing_key)
    response = client.post(
        "/api/v1/chat",
        headers={"X-API-Token": "test-token"},
        json={"provider": "gemini", "prompt": "Hello"},
    )
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_chat_requires_auth_config(monkeypatch) -> None:
    monkeypatch.delenv("APP_API_TOKEN", raising=False)
    response = client.post(
        "/api/v1/chat",
        headers={"X-API-Token": "anything"},
        json={"provider": "gemini", "prompt": "Hello"},
    )
    assert response.status_code == 503
