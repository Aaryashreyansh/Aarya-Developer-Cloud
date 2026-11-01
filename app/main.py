from fastapi import FastAPI

from app.ai.routes import router as ai_router

app = FastAPI(
    title="Aarya Developer Cloud",
    description="A multi-provider AI-assisted cloud developer workspace.",
    version="0.2.0",
)

app.include_router(ai_router, prefix="/api/v1")


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
