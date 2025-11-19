"""visualize.py
ASCII-based visualization helpers for VED results.
"""

from typing import Dict, List


def _bar(value: float, max_width: int = 40) -> str:
    if value < 0:
        value = 0.0
    if value > 1:
        value = 1.0
    length = int(round(value * max_width))
    return "#" * length + "-" * (max_width - length)


def print_outcome_distribution(outcome_counts: Dict[str, int]) -> None:
    total = sum(outcome_counts.values())
    if total == 0:
        print("No outcomes to display.")
        return
    print("Outcome distribution (normalized):")
    for label, count in outcome_counts.items():
        frac = count / total
        bar = _bar(frac)
        print(f"{label:10s} [{frac:5.2f}] {bar}")


def print_routing_cost_histogram(costs: List[float], bins: int = 10) -> None:
    if not costs:
        print("No routing costs to display.")
        return
    c_min = min(costs)
    c_max = max(costs)
    if c_min == c_max:
        print(f"All routing costs are identical: {c_min:.3f}")
        return
    width = (c_max - c_min) / bins
    hist = [0] * bins
    for c in costs:
        idx = int((c - c_min) / width)
        if idx == bins:
            idx -= 1
        hist[idx] += 1
    total = len(costs)
    print("Routing cost histogram:")
    for i in range(bins):
        lower = c_min + i * width
        upper = lower + width
        frac = hist[i] / total if total > 0 else 0.0
        bar = _bar(frac)
        print(f"[{lower:6.2f}, {upper:6.2f}) [{frac:5.2f}] {bar}")
