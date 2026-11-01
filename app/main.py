from fastapi import FastAPI

app = FastAPI(
    title="Aarya Developer Cloud",
    description="A starter API for an AI-assisted cloud developer workspace.",
    version="0.1.0",
)


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "name": "Aarya Developer Cloud",
        "status": "starter",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
