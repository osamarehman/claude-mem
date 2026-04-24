# claude-mem — Project Baseline

Version: **1.0.3**  
Date: 2026-04-24  
Repo: https://github.com/osamarehman/claude-mem  
PyPI: https://pypi.org/project/claude-mem/  

---

## What's in this repo

A zero-dependency Python CLI that gives Claude Code persistent session memory. It indexes `~/.claude/projects/` JSONL files into a local SQLite FTS5 database and injects ~50 tokens of context at the start of every new conversation via a `SessionStart` hook.

---

## Feature set (v1.0.3)

| Feature | File(s) |
|---|---|
| SessionBackend ABC | `backends/base.py` |
| Backend factory + auto-detect | `backends/__init__.py` |
| Claude Code JSONL reader | `backends/claude_code/reader.py` |
| FTS5 index builder + schema guard | `backends/claude_code/index.py` |
| Session path decoder | `backends/claude_code/detect.py` |
| Claude Code backend | `backends/claude_code/backend.py` |
| Surface detection + hook wiring | `backends/claude_code/install.py` |
| Health check (6 dimensions) | `backends/claude_code/health/` — index, freshness, corpus, latency, coverage, surfaces |
| AllBackend aggregator | `backends/all.py` |
| Cursor IDE backend | `backends/cursor.py` |
| Aider backend | `backends/aider.py` |
| `cc-index` command | `commands/index_cc.py` |
| `install-mode` command | `commands/install_mode.py` |
| `export` command | `commands/export.py` |
| `prune` command | `commands/prune.py` |
| `serve` command (MCP stdio) | `commands/serve.py` |
| MCP server (FastMCP) | `mcp_server.py` |
| Assistant message indexing | `index.py` — `assistant_summary` FTS5 column |
| CLI entrypoint | `__main__.py` — `prog="claude-mem"` |
| Stable JSON API docs | `docs/api.md` |
| CI matrix | `.github/workflows/ci.yml` — Python 3.10–3.13 × ubuntu/macos/windows |

---

## Test suite

**137 tests across 14 test files — all passing.**

| Test file | What it covers |
|---|---|
| `test_aider.py` | Aider backend — parser, search, health |
| `test_cc_detect.py` | Path encoding/decoding, session file discovery |
| `test_cc_index.py` | FTS5 index build, search, show, assistant_summary column |
| `test_cc_install.py` | Hook wiring, CLAUDE.md sentinel, MCP config wiring |
| `test_cc_reader.py` | JSONL parsing, assistant_summary truncation |
| `test_cursor.py` | Cursor backend — workspace DB parsing |
| `test_export.py` | Markdown and JSON export |
| `test_install_project.py` | CLAUDE.md write, idempotency, dry-run |
| `test_mcp_install.py` | wire_mcp_config — new file, idempotent, merge, dry-run |
| `test_parser.py` | CLI subcommand registration and TIER_MAP |
| `test_prune.py` | Old session removal, dry-run |
| `test_sanitize_terminal.py` | Unicode output safety |
| `test_telemetry.py` | Ring buffer, query hash, no raw query stored |

Run:
```bash
pytest src/session_recall/tests/ -q
```

---

## CLI commands

```bash
# Session recall
claude-mem list --json --limit 10
claude-mem files --json --days 7
claude-mem search "topic" --json
claude-mem show <session-id> --json

# Index management
claude-mem cc-index
claude-mem cc-index --rebuild
claude-mem cc-index --status
claude-mem prune --days 60

# Setup
claude-mem install-mode --setup
claude-mem install-mode --project
claude-mem install-mode --mcp
claude-mem install-mode --dry-run

# Export and health
claude-mem export --format md
claude-mem health --json

# MCP server
claude-mem serve
```

---

## Backends

```bash
claude-mem --backend claude list --json    # Claude Code (default)
claude-mem --backend cursor search "x"    # Cursor IDE
claude-mem --backend aider list --json    # Aider
claude-mem --backend all list --json      # all sources merged
```

---

## Repo commits

| Hash | Description |
|---|---|
| `5b2bad1` | docs: rewrite SESSION_TEST_BASELINE.md |
| `6e38f3a` | chore: rebrand all stale references to claude-mem |
| `9eb9caa` | docs: rewrite CONTRIBUTING.md |
| `564f152` | docs: rewrite README with original copy |
| `5339213` | chore: SEO — keywords, classifiers, v1.0.2 |
| `9187115` | feat: initial migration to claude-mem |

---

## Installation

```bash
pip install claude-mem
pip install "claude-mem[mcp]"    # with MCP server support
```

Requires Python 3.10+. Works on macOS, Linux, Windows.