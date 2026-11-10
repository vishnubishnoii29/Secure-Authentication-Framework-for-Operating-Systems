"""Deadlock detection and safe-state analysis.

Two methods are offered:

* Banker's algorithm: decides whether the state is *safe*, i.e. whether the
  processes can all finish in some order. An unsafe state is not yet a
  deadlock, but it cannot be guaranteed to stay free of one.
* Wait-for graph: a process waits for another when it still needs a resource
  type that is not free in the amount it needs and the other process holds it.
  A cycle means deadlock for single-instance resources; with several
  instances of a resource a cycle only means a *possible* deadlock.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set


@dataclass(slots=True)
class ResourceAllocationState:
    """Represents the current state of resource allocation."""

    num_processes: int
    num_resources: int
    allocated: List[List[int]]  # allocated[i][j] = resources allocated to process i
    max_demand: List[List[int]]  # max_demand[i][j] = max resources needed by process i
    available: List[int]  # available[j] = available resources of type j


@dataclass(slots=True)
class DeadlockDetectionResult:
    """Result of deadlock detection analysis."""

    is_deadlock: bool
    deadlocked_processes: Set[int]
    safe_sequence: List[int] | None
    need_matrix: List[List[int]]
    reason: str


def validate_state(state: ResourceAllocationState) -> None:
    """Raise ValueError when the state cannot describe a real system."""
    n, m = state.num_processes, state.num_resources
    if n <= 0 or m <= 0:
        raise ValueError("Deadlock detection requires at least one process and one resource.")
    if len(state.allocated) != n or len(state.max_demand) != n:
        raise ValueError("The matrices must have one row for each process.")
    if len(state.available) != m:
        raise ValueError(f"Available resources need exactly {m} values.")
    if any(v < 0 for v in state.available):
        raise ValueError("Available resources cannot be negative.")
    for i in range(n):
        if len(state.allocated[i]) != m or len(state.max_demand[i]) != m:
            raise ValueError("Every matrix row must have one value for each resource.")
        for j in range(m):
            if state.allocated[i][j] < 0 or state.max_demand[i][j] < 0:
                raise ValueError("Resource counts cannot be negative.")
            if state.allocated[i][j] > state.max_demand[i][j]:
                raise ValueError(
                    f"P{i} holds more of R{j} ({state.allocated[i][j]}) "
                    f"than its maximum demand ({state.max_demand[i][j]})."
                )


def _names(indices) -> str:
    return ", ".join(f"P{i}" for i in sorted(indices))


class DeadlockDetector:
    """Safe-state check (Banker's algorithm) and wait-for graph detection."""

    @staticmethod
    def _build_need_matrix(state: ResourceAllocationState) -> list[list[int]]:
        return [
            [state.max_demand[i][j] - state.allocated[i][j] for j in range(state.num_resources)]
            for i in range(state.num_processes)
        ]

    @staticmethod
    def _safety_check(
        state: ResourceAllocationState, need: list[list[int]]
    ) -> tuple[list[int], set[int]]:
        """Return (finishing order found, processes that can never finish)."""
        work = list(state.available)
        finish = [False] * state.num_processes
        order: list[int] = []

        progress = True
        while progress:
            progress = False
            for i in range(state.num_processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(state.num_resources)):
                    finish[i] = True
                    order.append(i)
                    for j in range(state.num_resources):
                        work[j] += state.allocated[i][j]
                    progress = True
                    break

        stuck = {i for i in range(state.num_processes) if not finish[i]}
        return order, stuck

    @staticmethod
    def detect_deadlock_bankers(state: ResourceAllocationState) -> DeadlockDetectionResult:
        """Banker's safety algorithm: a safe sequence exists, or the state is unsafe."""
        validate_state(state)
        need = DeadlockDetector._build_need_matrix(state)
        order, stuck = DeadlockDetector._safety_check(state, need)

        if stuck:
            return DeadlockDetectionResult(
                is_deadlock=True,
                deadlocked_processes=stuck,
                safe_sequence=None,
                need_matrix=need,
                reason=(
                    f"Unsafe state: {_names(stuck)} cannot be guaranteed to finish "
                    "with the resources that are free, so they may deadlock."
                ),
            )

        return DeadlockDetectionResult(
            is_deadlock=False,
            deadlocked_processes=set(),
            safe_sequence=order,
            need_matrix=need,
            reason=f"System is safe. Safe sequence: {[f'P{i}' for i in order]}",
        )

    @staticmethod
    def _wait_for_edges(
        state: ResourceAllocationState, need: list[list[int]]
    ) -> list[list[int]]:
        """Edge i -> k: i still needs a resource it cannot get now, and k holds it."""
        edges: list[list[int]] = [[] for _ in range(state.num_processes)]
        for i in range(state.num_processes):
            for j in range(state.num_resources):
                if need[i][j] > state.available[j]:
                    for k in range(state.num_processes):
                        if k != i and state.allocated[k][j] > 0 and k not in edges[i]:
                            edges[i].append(k)
        return edges

    @staticmethod
    def _cycle_members(edges: list[list[int]]) -> set[int]:
        """Processes on a cycle: members of a strongly connected group of 2 or more."""
        index_of: dict[int, int] = {}
        low: dict[int, int] = {}
        on_stack: set[int] = set()
        stack: list[int] = []
        members: set[int] = set()
        counter = 0

        def visit(node: int) -> None:
            nonlocal counter
            index_of[node] = low[node] = counter
            counter += 1
            stack.append(node)
            on_stack.add(node)
            for nxt in edges[node]:
                if nxt not in index_of:
                    visit(nxt)
                    low[node] = min(low[node], low[nxt])
                elif nxt in on_stack:
                    low[node] = min(low[node], index_of[nxt])
            if low[node] == index_of[node]:
                group: list[int] = []
                while True:
                    top = stack.pop()
                    on_stack.discard(top)
                    group.append(top)
                    if top == node:
                        break
                if len(group) > 1:
                    members.update(group)

        for start in range(len(edges)):
            if start not in index_of:
                visit(start)
        return members

    @staticmethod
    def detect_deadlock_wait_for_graph(
        state: ResourceAllocationState,
    ) -> DeadlockDetectionResult:
        """Build the wait-for graph from the current state and look for cycles."""
        validate_state(state)
        need = DeadlockDetector._build_need_matrix(state)
        edges = DeadlockDetector._wait_for_edges(state, need)
        cycle = DeadlockDetector._cycle_members(edges)

        if cycle:
            return DeadlockDetectionResult(
                is_deadlock=True,
                deadlocked_processes=cycle,
                safe_sequence=None,
                need_matrix=need,
                reason=(
                    f"Wait-for graph cycle among {_names(cycle)}. "
                    "This is a deadlock when each resource has a single instance; "
                    "with several instances, check it with Banker's algorithm too."
                ),
            )

        order, _ = DeadlockDetector._safety_check(state, need)
        return DeadlockDetectionResult(
            is_deadlock=False,
            deadlocked_processes=set(),
            safe_sequence=order if len(order) == state.num_processes else None,
            need_matrix=need,
            reason="No deadlock detected. The wait-for graph has no cycles.",
        )
