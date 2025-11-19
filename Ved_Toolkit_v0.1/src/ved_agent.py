"""ved_agent.py
Reference implementation of a VED-style agent.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

from ved_core import (
    Capacity,
    RoutingTopology,
    Outcome,
    Task,
    determine_outcome,
    ved_score,
    routing_cost,
)


@dataclass
class VEDAgent:
    """VED-style diagnostic agent with capacity and routing topology."""
    capacity: Capacity
    topology: RoutingTopology
    alpha: float = 1.0
    beta: float = 1.0
    gamma: float = 1.0

    outcomes: List[Outcome] = field(default_factory=list)
    routing_costs: List[float] = field(default_factory=list)

    def reset_history(self) -> None:
        self.outcomes.clear()
        self.routing_costs.clear()

    def evaluate_task(self, task: Task) -> Tuple[Outcome, float]:
        outcome = determine_outcome(task, self.capacity, self.topology)
        if outcome == Outcome.COLLAPSED:
            cost = 0.0
        else:
            cost = routing_cost(task.demand, self.capacity, self.topology)
        self.outcomes.append(outcome)
        self.routing_costs.append(cost)
        return outcome, cost

    def evaluate_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        self.reset_history()
        for t in tasks:
            self.evaluate_task(t)
        return self._build_summary()

    def _build_summary(self) -> Dict[str, Any]:
        total = len(self.outcomes)
        counts = {
            "RESOLVED": self.outcomes.count(Outcome.RESOLVED),
            "DEFERRED": self.outcomes.count(Outcome.DEFERRED),
            "COLLAPSED": self.outcomes.count(Outcome.COLLAPSED),
            "TRANSFORMED": self.outcomes.count(Outcome.TRANSFORMED),
        }
        score = ved_score(
            outcomes=self.outcomes,
            routing_costs=self.routing_costs,
            alpha=self.alpha,
            beta=self.beta,
            gamma=self.gamma,
        )
        return {
            "total_tasks": total,
            "outcome_counts": counts,
            "routing_costs": list(self.routing_costs),
            "ved_score": score,
        }
