# Architecture

## First iteration

```text
Developer
  |-- ChatGPT conversation: plan, generate, review, debug
  |-- GitHub: source of truth, pull requests, CI
  |-- Google Colab: optional notebook runtime
  '-- FastAPI service
        |-- /health
        '-- /docs
```

## Important integration boundary

A GitHub repository cannot itself attach a ChatGPT conversation to a live Colab kernel. The initial workflow is deliberately transparent and user-controlled:

1. Ask ChatGPT to design or modify code.
2. Commit code to GitHub.
3. Open the Colab notebook and run the relevant cells.
4. Review output and errors, then share them in the conversation.
5. Run automated tests in GitHub Actions.

A later AI adapter may call a provider API using a user-managed secret. Provider selection, pricing, quotas, and data handling must be reviewed before enabling it.

## Security principles

- Never commit credentials or tokens.
- Keep Colab notebooks free of embedded secrets and sensitive output.
- Do not build an endpoint that executes arbitrary code or shell commands.
- Require authentication and explicit approval before any future deployment or destructive operation.
- Use least-privilege GitHub tokens and repository secrets.
