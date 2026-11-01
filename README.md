# Aarya Developer Cloud

A cloud-first developer workspace starter connecting an AI-assisted workflow, Google Colab notebooks, GitHub version control, automated tests, and deployment-ready application structure.

## Project status

**Starter scaffold**. The repository is initialized with a FastAPI health-check service, tests, CI, environment template, and a Colab quickstart. AI-provider calls and deployment credentials are intentionally opt-in and are not included as hard-coded secrets.

## Architecture

- **ChatGPT**: planning, code review, debugging, and implementation guidance in this conversation.
- **Google Colab**: optional notebook execution and GPU/TPU workloads when available.
- **GitHub**: source control, issues, pull requests, and Actions CI.
- **FastAPI**: starter backend API.
- **Pytest**: automated tests.
- **Deployment**: add a hosting provider after the app is tested locally.

> ChatGPT is not automatically connected to a running Colab runtime by this repository. The notebook is a guided bridge: open it in Colab, run cells, and share outputs/errors here for review.

## Quick start

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

Open:
- API health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

Run tests:

```bash
pytest
```

## Google Colab

Open `notebooks/aarya_developer_cloud_quickstart.ipynb` in Google Colab. It installs the project dependencies and runs a small Python environment check. Colab sessions are temporary; commit important work to GitHub.

## Configuration and secrets

1. Copy `.env.example` to `.env` for local configuration.
2. Keep real API keys in local environment variables or a hosting provider's secret manager.
3. Never commit `.env`, API keys, access tokens, or service-account files.
4. Do not expose a secret in a Colab notebook output or public notebook.

## Repository layout

```text
app/                 FastAPI application
notebooks/           Google Colab quickstart
tests/               Automated tests
docs/                Architecture and setup notes
.github/workflows/   Continuous integration
```

## Roadmap

- [x] Initial backend scaffold and health endpoint
- [x] Pytest smoke test
- [x] GitHub Actions CI
- [x] Colab quickstart notebook
- [ ] Optional AI provider adapter (user supplies their own key)
- [ ] Project-specific frontend / workspace UI
- [ ] Deployment workflow after hosting target is chosen

## Safety

The starter API does not execute arbitrary shell commands or user-submitted code. Any future code-execution feature should run in an isolated, resource-limited environment with explicit approval.

## License

No license has been selected yet. Until one is added, normal copyright restrictions apply.
