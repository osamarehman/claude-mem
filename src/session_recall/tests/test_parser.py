"""Parser introspection tests — every subcommand has a TIER_MAP entry."""
from session_recall.__main__ import TIER_MAP, _build_parser


def test_tier_map_covers_all_subcommands():
    """Every registered subcommand must have a TIER_MAP entry."""
    known_commands = {"list", "files", "show", "search", "health"}
    missing = known_commands - set(TIER_MAP.keys())
    assert not missing, f"Subcommands missing from TIER_MAP: {missing}"


def test_parser_does_not_include_copilot_backend():
    """The --backend flag must not offer 'copilot' as a choice."""
    parser = _build_parser()
    backend_action = next(
        a for a in parser._actions if hasattr(a, "option_strings") and "--backend" in a.option_strings
    )
    assert "copilot" not in (backend_action.choices or []), \
        "copilot should not be a valid --backend choice in claude-mem"


def test_parser_includes_claude_backend():
    """The --backend flag must include 'claude'."""
    parser = _build_parser()
    backend_action = next(
        a for a in parser._actions if hasattr(a, "option_strings") and "--backend" in a.option_strings
    )
    assert "claude" in (backend_action.choices or [])
