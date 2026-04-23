"""Dim 3: Query latency — time list + show queries."""
import time
from ..db.connect import connect_ro
from ..config import DB_PATH
from .scoring import score_dim

HINT = "Check DB size or run PRAGMA integrity_check"


def check() -> dict:
    try:
        conn = connect_ro(DB_PATH)
        t0 = time.monotonic()
        conn.execute("SELECT id, summary FROM sessions ORDER BY created_at DESC LIMIT 10").fetchall()
        rows = conn.execute("SELECT id FROM sessions LIMIT 1").fetchone()
        if rows:
            sid = rows[0]
            conn.execute("SELECT turn_index FROM turns WHERE session_id = ? LIMIT 5", (sid,)).fetchall()
        elapsed_ms = (time.monotonic() - t0) * 1000
        conn.close()
    except Exception as e:
        return {"name": "Query Latency", "score": 0, "zone": "RED",
                "detail": str(e), "hint": HINT}
    result = score_dim(elapsed_ms, green_threshold=200, amber_threshold=500, higher_is_better=False)
    result.update({"name": "Query Latency", "detail": f"{elapsed_ms:.0f}ms", "hint": HINT})
    return result
