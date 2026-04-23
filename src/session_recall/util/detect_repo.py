"""Detect current repository from git remote or environment."""
import subprocess
import re


def detect_repo() -> str | None:
    """Return 'owner/repo' from git remote origin, or None."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if not url:
        return None
    # Handle SSH: git@github.com:owner/repo.git
    m = re.match(r"git@[^:]+:(.+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    # Handle HTTPS: https://github.com/owner/repo.git
    m = re.match(r"https?://[^/]+/(.+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    return None
