# claude-mem

**Claude Code gets amnesia every 20–30 turns. This fixes it.**

Zero-dependency Python CLI that gives Claude instant recall of past sessions — read-only, schema-checked, ~50 tokens per context injection.

[![PyPI](https://img.shields.io/pypi/v/claude-mem)](https://pypi.org/project/claude-mem/)
[![CI](https://github.com/osamarehman/claude-mem/actions/workflows/ci.yml/badge.svg)](https://github.com/osamarehman/claude-mem/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](pyproject.toml)

---

## Quickstart

```bash
pip install claude-mem
claude-mem cc-index --rebuild     # index your ~/.claude/projects/ sessions
claude-mem install-mode --setup   # wire SessionStart hook → auto-injects context on every new session
```

That's it. Every new Claude Code conversation now receives ~50 tokens of recent session context before you type a single word.

For per-project wiring (version-controlled, visible to teammates):

```bash
claude-mem install-mode --project  # adds a sentinel-guarded block to ./CLAUDE.md
```

---

## The Problem

Claude Code compacts every 20–30 turns. Each compaction leaves Claude slightly less oriented — which burns more tokens re-explaining your project, which triggers the next compaction sooner. It's a death spiral.

```
200,000  tokens — context window (theoretical max)
120,000  tokens — effective limit before quality degrades (~60%)
 -65,000  tokens — MCP tools
 -10,000  tokens — instruction files
=========
 ~45,000  tokens — what you actually have before coherence drops
```

**I timed it over a week: 68 minutes per day lost to re-orientation.**

---

## Before & After

**Without claude-mem** — new session on an ongoing project:

```
You: Fix the failing test in the auth module

Claude: Let me explore the project structure...
        find . -name "*.py" | head -50           ← 2K tokens
        grep -r "test.*auth" tests/              ← 5K tokens
        cat tests/test_auth.py                   ← 3K tokens
        ...which test is failing?

You: The token refresh edge case we were working on yesterday
```
*~16K tokens burned. 8 minutes. Claude still not oriented.*

**With claude-mem** — same scenario:

```
You: Fix the failing test in the auth module

Claude: [auto-recall injected at session start]
        → Last session: "token refresh race condition — one edge case
          still failing on expired token + network timeout combo"
        → Files: src/auth/refresh.py, tests/test_refresh_edge_cases.py

        I can see the failing test. Let me look at that specific case...
        cat tests/test_refresh_edge_cases.py     ← 1K tokens (targeted)
```
*~1K tokens. 30 seconds. Immediately productive.*

---

## How It Works

Claude Code writes every session to `~/.claude/projects/` as JSONL files. `claude-mem` builds a local SQLite FTS5 index over those files and injects a ~50-token summary at the start of each new session via a `SessionStart` hook.

```
~/.claude/settings.json
  SessionStart hook
       │
       ▼
  claude-mem CLI
  (pure Python, zero deps)
       │
       ▼
  ~/.claude/.sr-index.db
  (SQLite FTS5, built from ~/.claude/projects/ JSONL)
       │ never writes to Claude's own files
       ▼
  ~50 tokens injected into conversation context
```

- **Zero dependencies** — stdlib only (`sqlite3`, `json`, `argparse`, `pathlib`)
- **Read-only** on Claude's data — never modifies `~/.claude/projects/`
- **FTS5 full-text search** — finds sessions by content, not just recency
- **Assistant message indexing** — searches both what you asked *and* what Claude answered

---

## Commands

### Session recall

```bash
claude-mem list --json --limit 10          # recent sessions
claude-mem files --json --days 7           # recently touched files
claude-mem search "auth refactor" --json   # full-text search
claude-mem show <session-id> --json        # full session detail
```

### Index management

```bash
claude-mem cc-index                # incremental update
claude-mem cc-index --rebuild      # full rebuild from scratch
claude-mem cc-index --status       # index freshness and session count
claude-mem prune --days 90         # remove sessions older than N days
```

### Health check

```bash
claude-mem health                  # 6-dimension health dashboard
claude-mem health --json           # machine-readable output
```

### Installation wiring

```bash
claude-mem install-mode                    # detect Claude Code surfaces (CLI, VS Code, JetBrains, Desktop)
claude-mem install-mode --setup            # wire SessionStart hook into ~/.claude/settings.json
claude-mem install-mode --project          # write CLAUDE.md block (per-repo, version-controlled)
claude-mem install-mode --mcp              # wire MCP server into claude_desktop_config.json
claude-mem install-mode --dry-run          # preview all changes without writing
```

### Export

```bash
claude-mem export --format md --days 30    # export sessions to markdown
claude-mem export --format json            # export as JSON
claude-mem export --session <id>           # export one specific session
```

### MCP server (optional)

```bash
pip install "claude-mem[mcp]"
claude-mem serve                           # start stdio MCP server
claude-mem install-mode --mcp              # auto-wire into Claude Desktop
```

The MCP server exposes three tools — `session_list`, `session_search`, `session_show` — usable from any MCP-compatible host without shell access.

---

## Backends

`claude-mem` works with multiple session sources:

| Backend | Source | Flag |
|---|---|---|
| **Claude Code** (default) | `~/.claude/projects/*.jsonl` | `--backend claude` |
| **Cursor** | `workspaceStorage/*/state.vscdb` | `--backend cursor` |
| **Aider** | `.aider.chat.history.md` | `--backend aider` |
| **All** | Fan-out across all detected | `--backend all` |

```bash
claude-mem --backend all list --json       # query all sources at once
claude-mem --backend cursor search "auth"  # Cursor sessions only
```

---

## Tier System

Progressive disclosure — most prompts never need more than Tier 1.

| Tier | Tokens | Command |
|---|---|---|
| 1 — cheap scan | ~50 | `list`, `files` |
| 2 — focused recall | ~200 | `search` |
| 3 — full detail | ~500 | `show`, `export` |

---

## Installation

```bash
pip install claude-mem              # core (zero dependencies)
pip install "claude-mem[mcp]"       # with MCP server support
```

Requires Python 3.10+.

---

## What This Isn't

- Not a vector database — SQLite FTS5 only, no embeddings
- Not cross-machine sync — local index only
- Not a replacement for project docs — recalls *what you did*, not *how the system works*

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues, PRs, and docs improvements welcome.

## License

MIT
