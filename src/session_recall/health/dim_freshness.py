"""Dim 1: DB freshness — how recently was session-store.db modified."""
import os
import time
from ..config import DB_PATH
from .scoring import score_dim

HINT = "Use Copilot CLI — DB only updates from active sessions"


def check() -> dict:
    try:
        mtime = os.path.getmtime(DB_PATH)
        age_hours = (time.time() - mtime) / 3600
    except OSError:
        return {"name": "DB Freshness", "score": 0, "zone": "RED",
                "detail": "DB not found", "hint": HINT}
    result = score_dim(age_hours, green_threshold=24, amber_threshold=72, higher_is_better=False)
    result.update({"name": "DB Freshness", "detail": f"{age_hours:.1f}h old", "hint": HINT})
    return result
