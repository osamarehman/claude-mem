"""Configuration constants for claude-mem CLI."""
import os
from pathlib import Path

TELEMETRY_PATH = os.environ.get(
    "CLAUDE_MEM_TELEMETRY",
    str(Path.home() / ".claude" / ".claude-mem-stats.json"),
)
