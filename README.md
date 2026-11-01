# Aarya Developer Cloud

A cloud-first developer workspace starter connecting a multi-provider AI backend, Google Colab development notebooks, GitHub version control, automated tests, and Render hosting.

## Architecture

- **ChatGPT**: planning, code review, debugging, and implementation guidance in the conversation.
- **Google Colab**: temporary notebook runtime for development and remote API testing.
- **GitHub**: source control and GitHub Actions CI.
- **FastAPI**: backend with OpenAI, Gemini, Claude, and OpenRouter adapters.
- **Render**: public HTTPS backend hosting, subject to plan limits.

Colab is a development environment; it does not need to stay running for the Render backend to work. The notebook uses a Colab Secret for the app access token. Provider API keys remain on Render.

## Deploy to Render

This repository includes `render.yaml`.

1. In Render, choose **New → Blueprint**.
2. Connect GitHub and select `Aaryashreyansh/Aarya-Developer-Cloud`.
3. Create the service from the Blueprint.
4. In Render's **Environment** settings, add `APP_API_TOKEN` and the provider API key/model variables you intend to use.
5. Deploy and copy the HTTPS service URL.

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the full walkthrough.

## Google Colab

Open [the Colab quickstart notebook](https://colab.research.google.com/github/Aaryashreyansh/Aarya-Developer-Cloud/blob/main/notebooks/aarya_developer_cloud_quickstart.ipynb). Run it from top to bottom to clone the repo, install dependencies, run tests, and check the Render service.

In Colab's Secrets panel, add `AARYA_API_TOKEN` with the same private value as Render's `APP_API_TOKEN`. Do not paste secrets into notebook cells.

## Local development

Requires Python 3.10+.

```bash
git clone https://github.com/Aaryashreyansh/Aarya-Developer-Cloud.git
cd Aarya-Developer-Cloud
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests with `pytest -q`. The protected chat endpoint requires `APP_API_TOKEN` and a configured provider key/model.

## Security

- Never commit `.env`, API keys, app tokens, or service-account files.
- Store secrets in Render Environment settings or Colab Secrets as documented.
- The backend does not execute generated code or arbitrary shell commands.
- Public deployment should use authentication and cost controls. Provider usage can incur charges.
