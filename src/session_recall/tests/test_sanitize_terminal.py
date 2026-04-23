"""Tests for terminal-escape sanitization — H2 fix validation."""
from session_recall.util.format_output import sanitize_for_terminal


def test_strips_csi_color():
    """CSI color codes should be stripped."""
    assert sanitize_for_terminal('\x1b[31mred text\x1b[0m') == 'red text'


def test_strips_osc_title():
    """OSC title-set should be stripped entirely."""
    assert sanitize_for_terminal('hi\x1b]0;HACKED\x07there') == 'hithere'


def test_strips_osc_clipboard():
    """OSC 52 clipboard injection should be stripped."""
    assert sanitize_for_terminal('\x1b]52;c;ZXZpbA==\x07ok') == 'ok'


def test_strips_osc_hyperlink():
    """OSC 8 hyperlink should strip wrapper, keep visible text."""
    inp = '\x1b]8;;evil.com\x07github.com\x1b]8;;\x07'
    out = sanitize_for_terminal(inp)
    assert out == 'github.com'
    assert '\x1b' not in out


def test_strips_c0_controls():
    """NUL, BEL, BS, DEL should be stripped."""
    assert sanitize_for_terminal('a\x00b\x07c\x08d\x7f') == 'abcd'


def test_preserves_tab_newline_cr():
    """TAB, LF, CR are legitimate whitespace — must survive."""
    assert sanitize_for_terminal('a\tb\nc\rd') == 'a\tb\nc\rd'


def test_handles_none():
    """None input returns empty string."""
    assert sanitize_for_terminal(None) == ''


def test_unicode_passthrough():
    """Non-ASCII printable characters should pass through unchanged."""
    assert sanitize_for_terminal('café 日本 🎉') == 'café 日本 🎉'
