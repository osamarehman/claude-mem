# Contributing to claude-mem

Contributions are welcome — bug fixes, new features, docs improvements, or new backend support. Here's how to get started.

## Setup

```bash
git clone https://github.com/osamarehman/claude-mem.git
cd claude-mem
pip install -e ".[dev]"
pytest src/session_recall/tests/ -q
```

All 137 tests should pass on a clean checkout.

## What to Work On

Check the [open issues](https://github.com/osamarehman/claude-mem/issues) — anything labeled `good first issue` is a good starting point. Documentation fixes and test coverage improvements are always appreciated.

Larger ideas worth contributing:
- New backends (Windsurf, Zed, VS Code Chat)
- Cross-machine sync via S3 / GitHub Gist
- MCP server enhancements

## Code Conventions

- **Zero runtime dependencies** — stdlib only (`sqlite3`, `json`, `pathlib`, `argparse`). Optional extras (like `mcp`) must be guarded with `try/except ImportError`.
- **Small focused modules** — prefer extracting helpers over long functions
- **No comments explaining what the code does** — only comment the non-obvious *why*
- **Relative imports** within the `session_recall` package

## Adding a New Backend

1. Create `src/session_recall/backends/your_tool.py` implementing `SessionBackend` (see `backends/base.py`)
2. Implement all 6 abstract methods: `is_available`, `list_sessions`, `list_files`, `search`, `show_session`, `health`
3. Register in `backends/__init__.py` `_BACKEND_LOADERS`
4. Add to `AllBackend._BACKEND_SPECS` in `backends/all.py`
5. Add `--backend your-tool` to `__main__.py` choices
6. Add tests in `src/session_recall/tests/test_your_tool.py`

## Adding a New Command

1. Create `src/session_recall/commands/your_command.py` with `def run(args) -> int`
2. Register argparse subparser in `__main__.py` `_build_parser()`
3. Add dispatch in `__main__.py` `_dispatch()`
4. Add a `TIER_MAP` entry (`0` for ops, `1`–`3` for query tiers)
5. Add tests

## PR Checklist

- [ ] `pytest src/session_recall/tests/ -q` passes
- [ ] `ruff check src/` passes
- [ ] No new runtime dependencies
- [ ] Docs updated if behavior changed (README, `docs/api.md` for `--json` output changes)

## Questions

Open an issue — happy to help scope the work before you start.
