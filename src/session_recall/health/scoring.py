"""Health check scoring — GREEN/AMBER/RED zone logic."""
from __future__ import annotations


def score_dim(value: float, green_threshold: float, amber_threshold: float,
              higher_is_better: bool = True) -> dict:
    """Score a dimension. Returns {"score": 0-10, "zone": "GREEN"|"AMBER"|"RED"}.

    If higher_is_better=True: value >= green → GREEN, >= amber → AMBER, else RED.
    If higher_is_better=False: value <= green → GREEN, <= amber → AMBER, else RED.
    """
    if higher_is_better:
        if value >= green_threshold:
            zone, score = "GREEN", min(10, 7 + 3 * (value - green_threshold) / max(green_threshold, 1))
        elif value >= amber_threshold:
            zone, score = "AMBER", 4 + 3 * (value - amber_threshold) / max(green_threshold - amber_threshold, 1)
        else:
            zone, score = "RED", max(0, 3 * value / max(amber_threshold, 1))
    else:
        if value <= green_threshold:
            zone, score = "GREEN", min(10, 7 + 3 * (green_threshold - value) / max(green_threshold, 1))
        elif value <= amber_threshold:
            zone, score = "AMBER", 4 + 3 * (amber_threshold - value) / max(amber_threshold - green_threshold, 1)
        else:
            zone, score = "RED", max(0, 3 * amber_threshold / max(value, 1))
    return {"score": round(min(10, max(0, score)), 1), "zone": zone}


def overall_score(dims: list[dict]) -> float:
    """Overall score = min of scored dims (most severe wins). Dims with score=None are skipped."""
    if not dims:
        return 0.0
    scored = [d["score"] for d in dims if d.get("score") is not None]
    return min(scored) if scored else 0.0
