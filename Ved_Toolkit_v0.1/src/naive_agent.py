"""naive_agent.py
Baseline agent for comparison against VEDAgent.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ved_core import Capacity, Outcome, Task


@dataclass
class NaiveAgent:
    """A minimal agent that checks only capacity feasibility."""
    capacity: Capacity
    outcomes: List[Outcome] = field(default_factory=list)

    def reset_history(self) -> None:
        self.outcomes.clear()

    def evaluate_task(self, task: Task) -> Outcome:
        if self.capacity.can_handle(task.demand):
            outcome = Outcome.RESOLVED
        else:
            outcome = Outcome.COLLAPSED
        self.outcomes.append(outcome)
        return outcome

    def evaluate_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        self.reset_history()
        for t in tasks:
            self.evaluate_task(t)
        total = len(self.outcomes)
        counts = {
            "RESOLVED": self.outcomes.count(Outcome.RESOLVED),
            "COLLAPSED": self.outcomes.count(Outcome.COLLAPSED),
            "DEFERRED": 0,
            "TRANSFORMED": 0,
        }
        return {
            "total_tasks": total,
            "outcome_counts": counts,
        }
