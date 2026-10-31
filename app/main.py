import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import Settings, get_settings
from app.llm.errors import LLMConfigurationError, LLMUnavailable
from app.llm.factory import create_provider
from app.llm.reliable import AsyncReliableLLM
from app.llm.types import LLMRequest, Message
from app.schemas import ChatRequest

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> AsyncReliableLLM:
    return create_provider(settings)


LLMDep = Annotated[AsyncReliableLLM, Depends(get_llm)]

usage_totals = {
    "requests": 0,
    "input_tokens": 0,
    "output_tokens": 0,
    "estimated": False,
    "cost_usd": 0.0,
}

@app.get("/hello")
def say_hello():
    return "hello"

@app.get("/")
def say_root():
    return "You are on root page"

@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "timestamp": datetime.now(UTC).isoformat(),
    }
@app.get("/ready")
def ready(settings: SettingsDep):
    """Readiness: check whether PostgreSQL is reachable."""
    if not settings.database_url:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": "DATABASE_URL is not configured"},
        )

    try:
        with psycopg.connect(settings.database_url, connect_timeout=3) as connection:
            connection.execute("SELECT 1")

        return {"status": "ready", "database": "connected"}

    except psycopg.Error:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "unavailable"},
        )
@app.get("/usage")
def get_usage() -> dict:
    """Return token and estimated cost totals for this server session."""
    return usage_totals

def sse(data: dict, event: str | None = None) -> str:
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data)}\n\n"


@app.post("/chat")
async def chat(request: ChatRequest, provider: LLMDep) -> StreamingResponse:
    llm_request = LLMRequest(
        messages=tuple(Message(role=message.role, content=message.content) for message in request.messages),
        model=request.model,
    )

    async def event_stream() -> AsyncIterator[str]:
        usage = None
        try:
            async for chunk in provider.stream(llm_request):
                if chunk.text:
                    yield sse({"delta": chunk.text})
                if chunk.usage is not None:
                    usage = chunk.usage
        except (LLMUnavailable, LLMConfigurationError) as error:
            yield sse({"error": str(error)}, event="error")
        usage_data = usage or {"input_tokens": 0, "output_tokens": 0, "estimated": False}
        if hasattr(usage_data, "__dict__"):
            usage_data = usage_data.__dict__

        input_tokens = int(usage_data.get("input_tokens", 0))
        output_tokens = int(usage_data.get("output_tokens", 0))
        cost_usd = float(usage_data.get("cost_usd", 0.0))

        usage_totals["requests"] += 1
        usage_totals["input_tokens"] += input_tokens
        usage_totals["output_tokens"] += output_tokens
        usage_totals["estimated"] = usage_totals["estimated"] or bool(
            usage_data.get("estimated", False)
        )
        usage_totals["cost_usd"] += cost_usd
        yield sse(
            {
                "usage": usage_data,
                "cost_usd": cost_usd,
            },
            event="done",
        )

    return StreamingResponse(event_stream(), media_type="text/event-stream")