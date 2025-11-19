"""task_generator.py
Utility functions for generating task sets for VED evaluation.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import random
from ved_core import Task


def make_task(
    name: str,
    demand: List[float],
    metadata: Optional[Dict[str, Any]] = None
) -> Task:
    """Create a single deterministic vectorized task."""
    return Task(name=name, demand=demand, metadata=metadata or {})


def make_task_set(
    names: List[str],
    demand_vectors: List[List[float]],
    metadatas: Optional[List[Optional[Dict[str, Any]]]] = None
) -> List[Task]:
    """Create a set of tasks from lists of names and demand vectors."""
    if len(names) != len(demand_vectors):
        raise ValueError("Name count and demand vector count mismatch.")

    if metadatas is None:
        metadatas = [None] * len(names)

    tasks = []
    for n, dv, md in zip(names, demand_vectors, metadatas):
        tasks.append(make_task(n, dv, md))
    return tasks


def random_task(
    name: str,
    dim: int,
    max_demand: float = 1.0,
    seed: Optional[int] = None
) -> Task:
    """Generate a random vectorized task with each component in [0, max_demand]."""
    if seed is not None:
        random.seed(seed)
    demand = [random.random() * max_demand for _ in range(dim)]
    return Task(name=name, demand=demand, metadata={"generated": True})


def random_task_set(
    count: int,
    dim: int,
    max_demand: float = 1.0,
    seed: Optional[int] = None
) -> List[Task]:
    """Generate a list of randomly generated tasks."""
    if seed is not None:
        random.seed(seed)
    return [
        random_task(f"T{i+1}", dim=dim, max_demand=max_demand)
        for i in range(count)
    ]


def validate_dimensions(tasks: List[Task], dim: int) -> None:
    """Ensure all tasks are of dimension `dim`."""
    for t in tasks:
        if len(t.demand) != dim:
            raise ValueError(f"Task {t.name} has incorrect dimension.")
