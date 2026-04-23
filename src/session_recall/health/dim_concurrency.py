"""Dim 7: Concurrency health — SQLITE_BUSY rate from telemetry."""
import json
from pathlib import Path
from ..config import TELEMETRY_PATH
from .scoring import score_dim

HINT = "Increase busy_timeout or reduce concurrent use"


def check() -> dict:
    path = Path(TELEMETRY_PATH)
    if not path.exists():
        return {"name": "Concurrency", "score": 5, "zone": "AMBER",
                "detail": "No telemetry data yet", "hint": "Run session-recall a few times first"}
    try:
        entries = json.loads(path.read_text()).get("entries", [])
    except Exception:
        return {"name": "Concurrency", "score": 5, "zone": "AMBER",
                "detail": "Telemetry file unreadable", "hint": "Delete and let it regenerate"}
    if not entries:
        return {"name": "Concurrency", "score": 5, "zone": "AMBER",
                "detail": "Empty telemetry", "hint": "Run session-recall a few times first"}
    total_busy = sum(e.get("busy_hits", 0) for e in entries)
    busy_rate = (total_busy / len(entries)) * 100
    avg_attempts = sum(e.get("attempts", 1) for e in entries) / len(entries)
    durations = sorted(e.get("duration_ms", 0) for e in entries)
    p95_idx = int(len(durations) * 0.95)
    p95 = durations[min(p95_idx, len(durations) - 1)]

    result = score_dim(busy_rate, green_threshold=5, amber_threshold=20, higher_is_better=False)
    detail = f"busy={busy_rate:.1f}%, avg_attempts={avg_attempts:.2f}, p95={p95}ms, n={len(entries)}"
    result.update({"name": "Concurrency", "detail": detail, "hint": HINT})
    return result
