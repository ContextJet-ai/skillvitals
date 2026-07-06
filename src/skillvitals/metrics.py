"""Pure scoring functions. No I/O, no model calls."""


def trigger_metrics(results) -> dict:
    """results: list of {"should_fire": bool, "fired": bool}. Returns rates + P/R/F1."""
    tp = sum(1 for r in results if r["should_fire"] and r["fired"])
    fp = sum(1 for r in results if not r["should_fire"] and r["fired"])
    fn = sum(1 for r in results if r["should_fire"] and not r["fired"])
    tn = sum(1 for r in results if not r["should_fire"] and not r["fired"])
    pos = tp + fn
    neg = fp + tn
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / pos if pos else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "n": len(results),
        "recall": round(recall, 3),                          # fires when it should
        "false_fire_rate": round(fp / neg, 3) if neg else 0.0,  # fires when it shouldn't
        "precision": round(precision, 3),
        "f1": round(f1, 3),
    }


def efficacy_metrics(pairs) -> dict:
    """pairs: list of {"with": float, "without": float} judge scores (higher better)."""
    n = len(pairs)
    if not n:
        return {"n": 0, "win_rate": 0.0, "avg_delta": 0.0, "avg_with": None, "avg_without": None}
    wins = sum(1 for p in pairs if p["with"] > p["without"])
    ties = sum(1 for p in pairs if p["with"] == p["without"])
    deltas = [p["with"] - p["without"] for p in pairs]
    return {
        "n": n,
        "win_rate": round(wins / n, 3),
        "tie_rate": round(ties / n, 3),
        "avg_delta": round(sum(deltas) / n, 3),
        "avg_with": round(sum(p["with"] for p in pairs) / n, 3),
        "avg_without": round(sum(p["without"] for p in pairs) / n, 3),
    }
