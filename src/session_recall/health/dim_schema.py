"""Dim 2: Schema integrity — expected tables and columns present."""
from ..db.connect import connect_ro
from ..db.schema_check import schema_check
from ..config import DB_PATH

HINT = "Run `session-recall schema-check` for details"


def check() -> dict:
    try:
        conn = connect_ro(DB_PATH)
        problems = schema_check(conn)
        conn.close()
    except SystemExit:
        return {"name": "Schema Integrity", "score": 0, "zone": "RED",
                "detail": "DB connection failed", "hint": HINT}
    if not problems:
        return {"name": "Schema Integrity", "score": 10, "zone": "GREEN",
                "detail": "All tables/columns OK", "hint": ""}
    has_missing_table = any("MISSING TABLE" in p for p in problems)
    if has_missing_table:
        return {"name": "Schema Integrity", "score": 1, "zone": "RED",
                "detail": "; ".join(problems), "hint": HINT}
    return {"name": "Schema Integrity", "score": 5, "zone": "AMBER",
            "detail": "; ".join(problems), "hint": HINT}
