"""Dim 6: Repo coverage — sessions exist for the current repo."""
from ..db.connect import connect_ro
from ..config import DB_PATH
from ..util.detect_repo import detect_repo

HINT = "Run in a git repo or pass --repo all"


def check() -> dict:
    repo = detect_repo()
    if not repo:
        return {"name": "Repo Coverage", "score": 1, "zone": "RED",
                "detail": "Cannot detect repo from cwd", "hint": HINT}
    try:
        conn = connect_ro(DB_PATH)
        count = conn.execute(
            "SELECT COUNT(*) FROM sessions WHERE repository = ?", (repo,)
        ).fetchone()[0]
        conn.close()
    except Exception as e:
        return {"name": "Repo Coverage", "score": 0, "zone": "RED",
                "detail": str(e), "hint": HINT}
    if count >= 1:
        return {"name": "Repo Coverage", "score": 10, "zone": "GREEN",
                "detail": f"{count} sessions for {repo}", "hint": ""}
    return {"name": "Repo Coverage", "score": 5, "zone": "AMBER",
            "detail": f"0 sessions for {repo}", "hint": HINT}
