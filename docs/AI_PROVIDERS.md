# Multi-provider AI Brain

The API supports OpenAI Responses, Google Gemini generateContent, Anthropic Messages, and OpenRouter chat completions through a common server-side adapter.

## Server configuration

Set only the providers you intend to use as environment variables on the backend host:

- `APP_API_TOKEN` (required to use the chat endpoint)
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`

Set the matching model ID explicitly:

- `OPENAI_MODEL`
- `GEMINI_MODEL`
- `ANTHROPIC_MODEL`
- `OPENROUTER_MODEL`

Optional base URL overrides:

- `OPENAI_BASE_URL` (default: `https://api.openai.com/v1`)
- `ANTHROPIC_BASE_URL` (default: `https://api.anthropic.com`)
- `OPENROUTER_BASE_URL` (default: `https://openrouter.ai/api/v1`)

Model availability and pricing depend on the provider account. Choose model IDs shown in the provider's own console or documentation. No provider is assumed to be free or unlimited.

## Endpoints

- `GET /api/v1/providers`: list supported providers.
- `POST /api/v1/chat`: send a prompt to one provider. Requires the `X-API-Token` request header matching server-side `APP_API_TOKEN`.

Example request:

```http
POST /api/v1/chat
Content-Type: application/json
X-API-Token: <your-private-app-token>
```

```json
{
  "provider": "gemini",
  "prompt": "Explain this Python error",
  "system_prompt": "You are a careful coding assistant."
}
```

## Security and cost controls

- The app token protects the chat endpoint from unauthenticated public use. Keep it private and rotate it if exposed.
- Provider API keys stay on the server. Never place them in frontend JavaScript, notebook outputs, or committed files.
- Keep provider keys in hosting secrets or a local untracked `.env`.
- Add per-user quotas, rate limits, and monitoring before wider public use.
- Provider calls may incur charges and are subject to account quotas.
- The current endpoint is a minimal text adapter. It does not execute generated code, call tools, or autonomously modify repositories.
