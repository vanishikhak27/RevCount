# Root forwarder for compatibility with root uvicorn runs
from backend.app.main import app

__all__ = ["app"]
