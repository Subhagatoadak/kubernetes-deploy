from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None


app = FastAPI(
    title="Kubernetes Deploy Demo",
    version="0.1.0",
    description="Simple FastAPI backend to demonstrate Docker + Helm deployment.",
)


@app.get("/")
def read_root() -> dict:
    """Basic landing endpoint to confirm the service is reachable."""
    return {
        "message": "FastAPI is running. Visit /docs for interactive API.",
        "health": "/healthz",
    }


@app.get("/healthz")
def health() -> dict:
    """Lightweight health endpoint for liveness/readiness probes."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/items")
def create_item(item: Item) -> dict:
    """Echo endpoint to show request handling."""
    return {"received": item.model_dump(), "created_at": datetime.now(timezone.utc).isoformat()}
