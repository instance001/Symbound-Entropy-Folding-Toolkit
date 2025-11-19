"""example_basic_run.py
Minimal example for running VED vs Naive agents.
"""

import os
import sys

# Allow `python examples/example_basic_run.py` from repo root
THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(THIS_DIR, "..", "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from ved_simulation import run_ved_vs_naive
from visualize import print_outcome_distribution, print_routing_cost_histogram


def main() -> None:
    ved_summary, naive_summary = run_ved_vs_naive()

    print("=== VED Agent ===")
    print("Total tasks:", ved_summary["total_tasks"])
    print("VED score:", f"{ved_summary['ved_score']:.4f}")
    print_outcome_distribution(ved_summary["outcome_counts"])
    print_routing_cost_histogram(ved_summary["routing_costs"])

    print("\n=== Naive Agent ===")
    print("Total tasks:", naive_summary["total_tasks"])
    print_outcome_distribution(naive_summary["outcome_counts"])


if __name__ == "__main__":
    main()
