"""Schema validation against expected Copilot CLI session-store.db structure."""

EXPECTED_SCHEMA: dict[str, set[str]] = {
    "sessions": {"id", "repository", "branch", "summary", "created_at", "updated_at"},
    "turns": {"session_id", "turn_index", "user_message", "assistant_response", "timestamp"},
    "session_files": {"session_id", "file_path", "tool_name", "turn_index", "first_seen_at"},
    "session_refs": {"session_id", "ref_type", "ref_value", "turn_index", "created_at"},
    "checkpoints": {"session_id", "checkpoint_number", "title", "overview", "created_at"},
}


def schema_check(conn) -> list[str]:
    """Validate DB schema. Returns list of problems (empty = OK)."""
    problems: list[str] = []
    for table, expected_cols in EXPECTED_SCHEMA.items():
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        if not rows:
            problems.append(f"MISSING TABLE: {table}")
            continue
        actual = {r[1] if isinstance(r, tuple) else r["name"] for r in rows}
        missing = expected_cols - actual
        if missing:
            problems.append(f"{table}: missing columns {missing}")
    return problems
