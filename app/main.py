# from typing import Annotated

# from fastapi import Depends, FastAPI

# from app.config import Settings, get_settings

# app = FastAPI(title="Examate RAG starter", version="0.1.0")

# SettingsDep = Annotated[Settings, Depends(get_settings)]


# @app.get("/health")
# def health(settings: SettingsDep) -> dict:
#     """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
#     return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


# from datetime import UTC, datetime
# from typing import Annotated

# from fastapi import Depends, FastAPI

# from app.config import Settings, get_settings

# app = FastAPI(title="RevCount", version="0.2.0")

# SettingsDep = Annotated[Settings, Depends(get_settings)]


# @app.get("/health")
# def health(settings: SettingsDep) -> dict:
#     """Check that the API process is running."""
#     return {
#         "status": "ok",
#         "app": settings.app_name,
#         "environment": settings.environment,
#         "timestamp": datetime.now(UTC).isoformat(),
#     }



from datetime import UTC, datetime
from threading import Lock
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings

app = FastAPI(title="RevCount", version="0.2.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]

usage = {
    "requests": 0,
    "successful_requests": 0,
    "fallback_requests": 0,
    "input_tokens": 0,
    "output_tokens": 0,
}
usage_lock = Lock()


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


def record_usage(
    *,
    success: bool,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> None:
    """Record request counts and token usage safely."""
    with usage_lock:
        usage["requests"] += 1
        usage[
            "successful_requests" if success else "fallback_requests"
        ] += 1
        usage["input_tokens"] += input_tokens
        usage["output_tokens"] += output_tokens


@app.get("/")
def root() -> dict:
    """Return basic application information."""
    return {
        "app": "RevCount",
        "message": "RevCount API is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Check whether the API process is running."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.post("/api/ask")
def ask(request: AskRequest) -> dict:
    """Answer a question using Gemini with RevCount project context."""
    settings = get_settings()
    api_key = settings.gemini_api_key.strip()
    model = settings.gemini_model

    if not api_key:
        record_usage(success=False)
        return {
            "answer": (
                "AI service is not configured. "
                "Please check your Gemini API key."
            ),
            "source": "fallback",
        }

    project_context = """
You are RevCount, an AI-powered financial reporting assistant
for auto-sector reporters covering Indian two-wheeler companies,
including TVS Motor, Bajaj Auto, and Hero MotoCorp.

Your purpose is to help reporters understand quarterly results,
vehicle sales volumes, financial performance, and trends.

Rules:
1. Answer clearly and concisely.
2. Never invent financial figures, facts, or citations.
3. Do not claim to have searched reports or databases unless
   the application has actually provided that information.
4. If the question requires company data that has not been
   provided, clearly explain that the data is unavailable.
5. Distinguish general explanations from verified financial data.
6. Keep answers useful for business and financial reporting.
"""

    try:
        from google import genai

        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 60000},
        )

        response = client.interactions.create(
            model=model,
            input=(
                f"{project_context}\n\n"
                f"User question: {request.question}"
            ),
        )

        answer = (response.output_text or "").strip()

        if not answer:
            raise ValueError("Gemini returned an empty response.")

        metadata = response.usage

        input_tokens = (
            getattr(metadata, "total_input_tokens", 0) or 0
            if metadata
            else 0
        )
        output_tokens = (
            getattr(metadata, "total_output_tokens", 0) or 0
            if metadata
            else 0
        )

        record_usage(
            success=True,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        return {
            "answer": answer,
            "source": "gemini",
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            },
        }

    except Exception as exc:
        error_message = str(exc)

        if api_key:
            error_message = error_message.replace(
                api_key, "[REDACTED]"
            )

        print(
            f"Gemini request failed: "
            f"{type(exc).__name__}: {error_message}"
        )

        record_usage(success=False)

        return {
            "answer": (
                "I couldn't retrieve an AI answer right now. "
                "Please try again later."
            ),
            "source": "fallback",
        }


@app.get("/usage")
def get_usage() -> dict:
    """Return process-local request and token totals."""
    with usage_lock:
        snapshot = usage.copy()

    return {
        **snapshot,
        "total_tokens": (
            snapshot["input_tokens"] + snapshot["output_tokens"]
        ),
        "estimated_cost_usd": None,
        "cost_note": (
            "Cost is not calculated yet. Configure verified model "
            "pricing before reporting a cost estimate."
        ),
    }
