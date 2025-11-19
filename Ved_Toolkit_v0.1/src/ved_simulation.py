"""ved_simulation.py
Simulation utilities for the VED Toolkit v0.1.
"""

from typing import List, Tuple
from ved_core import Capacity, RoutingTopology
from ved_agent import VEDAgent
from naive_agent import NaiveAgent
from task_generator import random_task_set, validate_dimensions


def run_ved_vs_naive(
    dim: int = 3,
    task_count: int = 50,
    max_demand: float = 1.0,
    capacity_vector: List[float] = None,
    topology: RoutingTopology = None,
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 1.0,
    seed: int = 42,
) -> Tuple[dict, dict]:
    import random
    random.seed(seed)

    if capacity_vector is None:
        capacity_vector = [1.0] * dim

    if topology is None:
        topology = RoutingTopology(
            base_cost=1.0,
            bottleneck_indices=(),
            bottleneck_multiplier=2.0,
            max_cost=10.0,
        )

    tasks = random_task_set(count=task_count, dim=dim, max_demand=max_demand, seed=seed)
    validate_dimensions(tasks, dim=dim)

    capacity = Capacity(vector=capacity_vector)
    ved_agent = VEDAgent(capacity=capacity, topology=topology,
                         alpha=alpha, beta=beta, gamma=gamma)
    naive_agent = NaiveAgent(capacity=capacity)

    ved_summary = ved_agent.evaluate_tasks(tasks)
    naive_summary = naive_agent.evaluate_tasks(tasks)

    return ved_summary, naive_summary


def main() -> None:
    from visualize import print_outcome_distribution, print_routing_cost_histogram

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
