"""Server-side adapters for supported AI providers.

Keys are read only from environment variables. Never send provider keys to clients.
"""
from __future__ import annotations

import os
from typing import Any

import httpx


class ProviderConfigurationError(Exception):
    pass


class ProviderRequestError(Exception):
    pass


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ProviderConfigurationError(f"{name} is not configured on the server.")
    return value


async def _post_json(
    url: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> dict[str, Any]:
    timeout = httpx.Timeout(60.0, connect=10.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        # Do not echo response bodies: they may contain provider diagnostics or sensitive data.
        raise ProviderRequestError(
            f"Provider request failed with HTTP {exc.response.status_code}."
        ) from None
    except (httpx.TimeoutException, httpx.RequestError, ValueError):
        raise ProviderRequestError("Provider request failed. Check connectivity and server logs.") from None


async def generate(
    provider: str,
    prompt: str,
    *,
    system_prompt: str | None = None,
    model: str | None = None,
) -> str:
    provider = provider.lower().strip()

    if provider == "openai":
        key = _required_env("OPENAI_API_KEY")
        chosen_model = model or os.getenv("OPENAI_MODEL", "gpt-6")
        payload: dict[str, Any] = {"model": chosen_model, "input": prompt}
        if system_prompt:
            payload["instructions"] = system_prompt
        data = await _post_json(
            os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/responses",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            payload=payload,
        )
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        pieces: list[str] = []
        for item in data.get("output", []):
            for part in item.get("content", []):
                if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    pieces.append(part["text"])
        if pieces:
            return "\n".join(pieces)
        raise ProviderRequestError("OpenAI returned no text output.")

    if provider == "gemini":
        key = _required_env("GEMINI_API_KEY")
        chosen_model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        payload = {"contents": contents}
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        data = await _post_json(
            f"https://generativelanguage.googleapis.com/v1beta/models/{chosen_model}:generateContent",
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            payload=payload,
        )
        try:
            return "\n".join(
                part["text"]
                for part in data["candidates"][0]["content"]["parts"]
                if isinstance(part.get("text"), str)
            )
        except (KeyError, IndexError, TypeError):
            raise ProviderRequestError("Gemini returned no text output.") from None

    if provider == "claude":
        key = _required_env("ANTHROPIC_API_KEY")
        chosen_model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        messages = [{"role": "user", "content": prompt}]
        payload = {"model": chosen_model, "max_tokens": 2048, "messages": messages}
        if system_prompt:
            payload["system"] = system_prompt
        data = await _post_json(
            os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/") + "/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": os.getenv("ANTHROPIC_VERSION", "2023-06-01"),
                "Content-Type": "application/json",
            },
            payload=payload,
        )
        try:
            return "\n".join(
                part["text"] for part in data["content"]
                if part.get("type") == "text" and isinstance(part.get("text"), str)
            )
        except (KeyError, TypeError):
            raise ProviderRequestError("Claude returned no text output.") from None

    if provider == "openrouter":
        key = _required_env("OPENROUTER_API_KEY")
        chosen_model = model or os.getenv("OPENROUTER_MODEL", "")
        if not chosen_model:
            raise ProviderConfigurationError("Set OPENROUTER_MODEL to a model available to your account.")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = await _post_json(
            os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/") + "/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("APP_PUBLIC_URL", "http://localhost:8000"),
                "X-Title": "Aarya Developer Cloud",
            },
            payload={"model": chosen_model, "messages": messages},
        )
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise ProviderRequestError("OpenRouter returned no text output.") from None

    raise ProviderConfigurationError(
        "Unknown provider. Choose openai, gemini, claude, or openrouter."
    )
