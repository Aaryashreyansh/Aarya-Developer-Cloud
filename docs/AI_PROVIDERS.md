# Multi-provider AI Brain

The API supports OpenAI Responses, Google Gemini generateContent, Anthropic Messages, and OpenRouter chat completions through a common server-side adapter.

## Configure keys

Set only the providers you intend to use as environment variables on the backend host:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`

Optional model overrides:

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

- `GET /api/v1/providers`: list supported providers (does not disclose configured secrets).
- `POST /api/v1/chat`: send a prompt to one provider.

Example request:

```json
{
  "provider": "gemini",
  "prompt": "Explain this Python error",
  "system_prompt": "You are a careful coding assistant."
}
```

Example response:

```json
{
  "provider": "gemini",
  "model": null,
  "text": "..."
}
```

## Security and cost controls

- API keys stay on the server. Never place them in frontend JavaScript, notebook outputs, or committed files.
- Keep provider keys in hosting secrets or a local untracked `.env`.
- Add authentication, per-user quotas, rate limits, and request logging before exposing this API publicly.
- Provider calls may incur charges and are subject to account quotas.
- The current endpoint is a minimal text adapter. It does not execute generated code, call tools, or autonomously modify repositories.
