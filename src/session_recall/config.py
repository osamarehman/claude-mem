"""Configuration constants for auto-memory CLI."""
import os
from pathlib import Path

DB_PATH = os.environ.get(
    "SESSION_RECALL_DB",
    str(Path.home() / ".copilot" / "session-store.db"),
)

TELEMETRY_PATH = os.environ.get(
    "SESSION_RECALL_TELEMETRY",
    str(Path.home() / ".copilot" / "scripts" / ".session-recall-stats.json"),
)

RETRY_DELAYS_MS = [50, 150, 450]
MAX_RETRIES = len(RETRY_DELAYS_MS)

EXPECTED_SCHEMA_VERSION = 1
