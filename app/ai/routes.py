import hmac
import os
from typing import Literal

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.ai.providers import (
    ProviderConfigurationError,
    ProviderRequestError,
    generate,
)

router = APIRouter(tags=["AI"])


class ChatRequest(BaseModel):
    provider: Literal["openai", "gemini", "claude", "openrouter"] = "gemini"
    prompt: str = Field(min_length=1, max_length=12000)
    system_prompt: str | None = Field(default=None, max_length=4000)
    model: str | None = Field(default=None, max_length=120)


class ChatResponse(BaseModel):
    provider: str
    model: str | None
    text: str


@router.get("/providers")
def list_providers() -> dict[str, list[dict[str, str]]]:
    """List supported providers without exposing whether secrets are configured."""
    return {
        "providers": [
            {"id": "openai", "name": "OpenAI"},
            {"id": "gemini", "name": "Google Gemini"},
            {"id": "claude", "name": "Anthropic Claude"},
            {"id": "openrouter", "name": "OpenRouter"},
        ]
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    x_api_token: str | None = Header(default=None, alias="X-API-Token"),
) -> ChatResponse:
    expected_token = os.getenv("APP_API_TOKEN", "").strip()
    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="Backend authentication is not configured. Set APP_API_TOKEN on the server.",
        )
    if not x_api_token or not hmac.compare_digest(x_api_token, expected_token):
        raise HTTPException(status_code=401, detail="Invalid or missing API token.")

    try:
        answer = await generate(
            request.provider,
            request.prompt,
            system_prompt=request.system_prompt,
            model=request.model,
        )
        return ChatResponse(provider=request.provider, model=request.model, text=answer)
    except ProviderConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except ProviderRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from None
