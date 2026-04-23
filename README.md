# claude-mem

**Persistent session memory for Claude Code. Zero dependencies. ~50 tokens.**

Every time Claude Code starts a new conversation, it starts cold — no memory of what you built yesterday, which files you touched, or what decisions you made. `claude-mem` solves this by indexing your Claude session history locally and injecting the relevant context automatically at the start of each conversation.

[![PyPI](https://img.shields.io/pypi/v/claude-mem)](https://pypi.org/project/claude-mem/)
[![CI](https://github.com/osamarehman/claude-mem/actions/workflows/ci.yml/badge.svg)](https://github.com/osamarehman/claude-mem/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](pyproject.toml)

---

## The Problem

Claude Code stores every conversation under `~/.claude/projects/` as JSONL files, but it never reads them back. Start a new session and you're back to square one — Claude doesn't know what branch you're on, which bug you were chasing, or that you already tried the obvious approach and it didn't work.

The result: the first 5–10 minutes of every session go toward re-orienting Claude. Multiply that by every session across every project and it adds up fast.

---

## How claude-mem Fixes It

`claude-mem` reads those JSONL files, builds a local SQLite FTS5 index, and wires a `SessionStart` hook into `~/.claude/settings.json`. When a new Claude Code conversation opens, the hook runs `claude-mem list --json` and injects a compact summary of your recent sessions — what you were working on, which files you touched, where you left off. The whole injection is around 50 tokens.

```
New Claude session opens
        │
        ▼
SessionStart hook fires
        │
        ▼
claude-mem reads ~/.claude/.sr-index.db
        │
        ▼
~50-token summary injected into context
  "Last session: fixed token refresh race condition in
   src/auth/refresh.py — edge case test still failing"
        │
        ▼
Claude is immediately oriented. No re-exploration needed.
```

---

## Quickstart

```bash
pip install claude-mem
claude-mem cc-index                   # build the index from your session history
claude-mem install-mode --setup       # wire the SessionStart hook
```

Done. The next Claude Code session you open will have context from your previous work.

To add per-project memory (checked into your repo, visible to your team):

```bash
claude-mem install-mode --project     # writes a sentinel-guarded block to CLAUDE.md
```

---

## Commands

### Query your session history

```bash
claude-mem list --json --limit 10          # recent sessions with summaries
claude-mem files --json --days 7           # files you've been working on
claude-mem search "database migration"     # full-text search across all sessions
claude-mem show <session-id> --json        # full conversation detail
```

### Manage the index

```bash
claude-mem cc-index                        # incremental update (fast)
claude-mem cc-index --rebuild              # full rebuild from scratch
claude-mem cc-index --status               # check index health and freshness
claude-mem prune --days 60                 # clean up old sessions
```

### Hook and integration setup

```bash
claude-mem install-mode                    # see what Claude Code surfaces are detected
claude-mem install-mode --setup            # wire global SessionStart hook
claude-mem install-mode --project          # add CLAUDE.md block to current repo
claude-mem install-mode --mcp              # wire as MCP server in Claude Desktop
claude-mem install-mode --dry-run          # preview any of the above without writing
```

### Export and health

```bash
claude-mem export --format md --days 30    # export sessions to markdown
claude-mem export --format json            # export as JSON
claude-mem health                          # 6-dimension health check
```

---

## MCP Server

`claude-mem` can run as an MCP tool server, making your session history queryable from Claude Desktop or any MCP-compatible host:

```bash
pip install "claude-mem[mcp]"
claude-mem install-mode --mcp              # writes entry to claude_desktop_config.json
```

Three tools are exposed: `session_list`, `session_search`, `session_show`.

---

## Multiple Backends

Beyond Claude Code, `claude-mem` can also read session history from other tools:

| Backend | Reads from |
|---|---|
| `claude` (default) | `~/.claude/projects/*.jsonl` |
| `cursor` | Cursor workspace SQLite databases |
| `aider` | `.aider.chat.history.md` files |
| `all` | All of the above, merged |

```bash
claude-mem --backend all list --json
claude-mem --backend cursor search "refactor"
```

---

## Design

- **Read-only** — never writes to Claude's own files under `~/.claude/projects/`
- **Zero dependencies** — pure Python stdlib (`sqlite3`, `json`, `pathlib`, `argparse`)
- **FTS5 full-text search** — indexes both your messages and Claude's responses
- **Progressive disclosure** — `list` costs ~50 tokens, `search` ~200, `show` ~500
- **Incremental indexing** — only processes new sessions since the last run

---

## Installation

```bash
pip install claude-mem              # zero-dependency core
pip install "claude-mem[mcp]"       # with MCP server support
```

Requires Python 3.10+. Works on macOS, Linux, and Windows.

---

## Contributing

Issues and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
