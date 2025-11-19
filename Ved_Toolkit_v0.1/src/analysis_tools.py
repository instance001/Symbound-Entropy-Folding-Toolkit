"""analysis_tools.py
Supplementary analysis utilities for the VED Toolkit.
"""

from typing import List, Dict
import math


def shannon_entropy(probabilities: List[float]) -> float:
    total = sum(probabilities)
    if total == 0:
        return 0.0
    H = 0.0
    for p in probabilities:
        if p > 0:
            p_norm = p / total
            H -= p_norm * math.log2(p_norm)
    return H


def outcome_entropy(outcome_counts: Dict[str, int]) -> float:
    counts = list(outcome_counts.values())
    return shannon_entropy(counts)


def normalized_entropy(outcome_counts: Dict[str, int]) -> float:
    H = outcome_entropy(outcome_counts)
    K = len(outcome_counts)
    if K <= 1:
        return 0.0
    return H / math.log2(K)


def stability_ratio(resolved: int, collapsed: int) -> float:
    total = resolved + collapsed
    if total == 0:
        return 1.0
    return resolved / total


def drift_pressure(deferred: int, transformed: int) -> float:
    return deferred + transformed


def spatial_gradient(demand_vector: List[float]) -> float:
    if not demand_vector:
        return 0.0
    mean = sum(demand_vector) / len(demand_vector)
    return math.sqrt(sum((x - mean) ** 2 for x in demand_vector))


def temporal_smoothing(previous_pressure: float, new_pressure: float) -> float:
    return abs(previous_pressure - new_pressure)


def aggregate_runs(run_summaries: List[Dict]) -> Dict:
    if not run_summaries:
        return {}
    cumulative = {}
    entropies = []
    stabilities = []
    for s in run_summaries:
        oc = s.get("outcome_counts", {})
        for k, v in oc.items():
            cumulative[k] = cumulative.get(k, 0) + v
        if oc:
            entropies.append(outcome_entropy(oc))
        res = oc.get("RESOLVED", 0)
        col = oc.get("COLLAPSED", 0)
        stabilities.append(stability_ratio(res, col))
    avg_entropy = sum(entropies) / len(entropies) if entropies else 0.0
    avg_stability = sum(stabilities) / len(stabilities) if stabilities else 0.0
    return {
        "cumulative_counts": cumulative,
        "avg_entropy": avg_entropy,
        "avg_stability": avg_stability,
    }
