# Deployment: Render + Google Colab

## Render: public FastAPI backend

This repository includes a `render.yaml` Blueprint.

1. Sign in to Render and choose **New → Blueprint**.
2. Connect GitHub and select `Aaryashreyansh/Aarya-Developer-Cloud`.
3. Review the Blueprint and create the service.
4. In the service dashboard, open **Environment** and add:
   - `APP_API_TOKEN`: a long, randomly generated private token. Do not commit it.
   - One or more provider keys: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or `OPENROUTER_API_KEY`.
   - The corresponding model ID variable, for example `OPENAI_MODEL` or `GEMINI_MODEL`, using a model enabled for your provider account.
5. Save and deploy. Render reads the port from `PORT` and checks `/health`.
6. Copy the service's HTTPS URL from the Render dashboard.

The free service plan may sleep or have resource/usage limits. It is not a 24/7 uptime guarantee. Check current plan limits and pricing in Render before relying on it.

## Google Colab: development and remote API tests

1. Open `notebooks/aarya_developer_cloud_quickstart.ipynb` in Colab.
2. Run the cells from top to bottom. The notebook clones this GitHub repository and runs the test suite in the temporary Colab runtime.
3. In Colab's **Secrets** panel, create `AARYA_API_TOKEN` with the same value as Render's `APP_API_TOKEN`. Grant the notebook access.
4. Run the remote health/provider check cell and enter the Render HTTPS base URL when prompted.
5. The optional chat smoke test sends a small prompt to the selected provider through Render. Provider API keys stay on Render, not in Colab.

Do not paste API tokens into notebook cells, source files, screenshots, or chat messages. Do not print secret values.

## Local development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -q
```

Set `APP_API_TOKEN` and the provider key/model environment variables in your local shell before calling the protected chat endpoint.

## Deployment boundary

Colab is an interactive, temporary development runtime. Render is the persistent web-hosting target (subject to plan limits). Colab does not need to stay running for the Render service to work.
