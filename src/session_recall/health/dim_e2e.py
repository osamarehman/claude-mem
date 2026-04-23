"""Dim 8: E2E probe — list → show → parse succeeds."""
from ..db.connect import connect_ro
from ..config import DB_PATH

HINT = "Check exit code and stderr from individual commands"


def check() -> dict:
    try:
        conn = connect_ro(DB_PATH)
        # Step 1: list
        sessions = conn.execute(
            "SELECT id, summary FROM sessions ORDER BY created_at DESC LIMIT 1"
        ).fetchall()
        if not sessions:
            conn.close()
            return {"name": "E2E Probe", "score": 5, "zone": "AMBER",
                    "detail": "No sessions found", "hint": "Use Copilot CLI first"}
        # Step 2: show (drill into first session)
        sid = sessions[0]["id"]
        turns = conn.execute(
            "SELECT turn_index FROM turns WHERE session_id = ? LIMIT 3", (sid,)
        ).fetchall()
        conn.close()
        return {"name": "E2E Probe", "score": 10, "zone": "GREEN",
                "detail": f"list→show OK (session {sid[:8]}, {len(turns)} turns sampled)",
                "hint": ""}
    except Exception as e:
        return {"name": "E2E Probe", "score": 0, "zone": "RED",
                "detail": str(e), "hint": HINT}
