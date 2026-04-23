"""Tests for health/scoring.py — zone scoring and overall calculation."""
from session_recall.health.scoring import score_dim, overall_score


def test_green_zone_higher_is_better():
    r = score_dim(100, green_threshold=50, amber_threshold=10)
    assert r["zone"] == "GREEN"
    assert r["score"] >= 7.0


def test_amber_zone_higher_is_better():
    r = score_dim(30, green_threshold=50, amber_threshold=10)
    assert r["zone"] == "AMBER"
    assert 4.0 <= r["score"] < 7.0


def test_red_zone_higher_is_better():
    r = score_dim(5, green_threshold=50, amber_threshold=10)
    assert r["zone"] == "RED"
    assert r["score"] < 4.0


def test_green_zone_lower_is_better():
    r = score_dim(10, green_threshold=24, amber_threshold=72, higher_is_better=False)
    assert r["zone"] == "GREEN"
    assert r["score"] >= 7.0


def test_red_zone_lower_is_better():
    r = score_dim(100, green_threshold=24, amber_threshold=72, higher_is_better=False)
    assert r["zone"] == "RED"
    assert r["score"] < 4.0


def test_overall_score_min():
    dims = [{"score": 10}, {"score": 5}, {"score": 8}]
    assert overall_score(dims) == 5


def test_overall_score_empty():
    assert overall_score([]) == 0.0


def test_score_clamped_0_10():
    r = score_dim(0, green_threshold=50, amber_threshold=10)
    assert 0 <= r["score"] <= 10
    r = score_dim(99999, green_threshold=50, amber_threshold=10)
    assert 0 <= r["score"] <= 10


def test_overall_score_skips_none():
    """Dim with score=None (e.g. Dim 9 in CALIBRATING) must be skipped, not crash."""
    dims = [{"score": None, "zone": "CALIBRATING"}, {"score": 8, "zone": "GREEN"}]
    assert overall_score(dims) == 8


def test_overall_score_all_none():
    """If every dim is calibrating, overall is 0.0 (no signal yet)."""
    dims = [{"score": None}, {"score": None}]
    assert overall_score(dims) == 0.0
