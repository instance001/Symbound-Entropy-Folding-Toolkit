"""ved_core.py
Core data structures and primitive operations for the VED Toolkit v0.1.
Implements:
- Task representation
- Outcome enumeration
- Capacity vector handling
- Basic routing and outcome logic (domain-agnostic)
- Composite VED score
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any
import math


class Outcome(Enum):
    RESOLVED = 1
    DEFERRED = 2
    COLLAPSED = 3
    TRANSFORMED = 4


@dataclass
class Task:
    """Represents a vectorized task."""
    name: str
    demand: List[float]     # demand vector D_i
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Capacity:
    """Represents the capacity vector C."""
    vector: List[float]

    def can_handle(self, demand: List[float]) -> bool:
        """Check capacity feasibility: D_i <= C component-wise."""
        if len(demand) != len(self.vector):
            raise ValueError("Dimension mismatch between demand and capacity.")
        return all(d <= c for d, c in zip(demand, self.vector))

    def utilization(self, demand_matrix: List[List[float]]) -> List[float]:
        """Compute utilization ratios L_j / c_j."""
        if not demand_matrix:
            return [0.0] * len(self.vector)
        load = [0.0] * len(self.vector)
        for d in demand_matrix:
            if len(d) != len(self.vector):
                raise ValueError("Dimension mismatch in demand matrix.")
            for j in range(len(self.vector)):
                load[j] += d[j]
        return [load[j] / self.vector[j] if self.vector[j] > 0 else math.inf
                for j in range(len(self.vector))]


@dataclass
class RoutingTopology:
    """Structured description of routing parameters."""
    base_cost: float = 1.0
    bottleneck_indices: Tuple[int, ...] = ()
    bottleneck_multiplier: float = 2.0
    max_cost: float = 10.0


def routing_cost(
    demand: List[float],
    capacity: Capacity,
    topology: RoutingTopology
) -> float:
    """Domain-agnostic routing cost function."""
    cvec = capacity.vector
    if len(demand) != len(cvec):
        raise ValueError("Dimension mismatch between demand and capacity vectors.")

    # Base cost
    cost = topology.base_cost

    # Fractional load contribution
    for j in range(len(demand)):
        if cvec[j] == 0:
            return math.inf
        cost += demand[j] / cvec[j]

    # Bottleneck penalties
    for j in topology.bottleneck_indices:
        cost += topology.bottleneck_multiplier * (demand[j] / cvec[j])

    return cost


def determine_outcome(
    task: Task,
    capacity: Capacity,
    topology: RoutingTopology
) -> Outcome:
    """Determine outcome class for a given task using VED rules."""
    if not capacity.can_handle(task.demand):
        return Outcome.COLLAPSED

    cost = routing_cost(task.demand, capacity, topology)

    if cost > topology.max_cost:
        return Outcome.DEFERRED

    return Outcome.RESOLVED


def ved_score(
    outcomes: List[Outcome],
    routing_costs: List[float],
    alpha: float,
    beta: float,
    gamma: float
) -> float:
    """Compute S_VED = α E_o + β E_r + γ (1 - F)."""
    total = len(outcomes)
    if total == 0:
        return 0.0

    resolved = outcomes.count(Outcome.RESOLVED)
    failed = outcomes.count(Outcome.COLLAPSED)

    E_o = resolved / total

    W = resolved  # simplification: resolved tasks = 'work' units
    R_total = sum(routing_costs) if routing_costs else 0.0
    E_r = W / (W + R_total) if (W + R_total) > 0 else 0.0

    F = failed / total

    return alpha * E_o + beta * E_r + gamma * (1 - F)
