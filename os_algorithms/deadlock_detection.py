"""Deadlock Detection and Resource Allocation Algorithm."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set


@dataclass
class ResourceAllocationState:
    """Represents the current state of resource allocation."""

    num_processes: int
    num_resources: int
    allocated: List[List[int]]  # allocated[i][j] = resources allocated to process i
    max_demand: List[List[int]]  # max_demand[i][j] = max resources needed by process i
    available: List[int]  # available[j] = available resources of type j


@dataclass
class DeadlockDetectionResult:
    """Result of deadlock detection analysis."""

    is_deadlock: bool
    deadlocked_processes: Set[int]
    safe_sequence: List[int] | None
    need_matrix: List[List[int]]
    reason: str


class DeadlockDetector:
    """Deadlock detection using Banker's Algorithm and cycle detection."""

    @staticmethod
    def _build_need_matrix(state: ResourceAllocationState) -> list[list[int]]:
        return [
            [state.max_demand[i][j] - state.allocated[i][j] for j in range(state.num_resources)]
            for i in range(state.num_processes)
        ]

    @staticmethod
    def detect_deadlock_bankers(state: ResourceAllocationState) -> DeadlockDetectionResult:
        """
        Detect deadlock using Banker's Algorithm.
        Returns safe sequence if exists, otherwise indicates deadlock.
        """
        need = DeadlockDetector._build_need_matrix(state)
        work = list(state.available)
        finish = [False] * state.num_processes
        safe_sequence: list[int] = []

        for _ in range(state.num_processes):
            found = False

            for i in range(state.num_processes):
                if finish[i]:
                    continue

                if all(need[i][j] <= work[j] for j in range(state.num_resources)):
                    safe_sequence.append(i)
                    finish[i] = True
                    for j in range(state.num_resources):
                        work[j] += state.allocated[i][j]
                    found = True
                    break

            if not found:
                deadlocked = {i for i in range(state.num_processes) if not finish[i]}
                return DeadlockDetectionResult(
                    is_deadlock=True,
                    deadlocked_processes=deadlocked,
                    safe_sequence=None,
                    need_matrix=need,
                    reason=f"Deadlock detected! Processes {deadlocked} are stuck.",
                )

        return DeadlockDetectionResult(
            is_deadlock=False,
            deadlocked_processes=set(),
            safe_sequence=safe_sequence,
            need_matrix=need,
            reason=f"System is safe! Safe sequence: {[f'P{i}' for i in safe_sequence]}",
        )

    @staticmethod
    def detect_deadlock_wait_for_graph(
        state: ResourceAllocationState,
    ) -> DeadlockDetectionResult:
        """
        Detect deadlock using Wait-for Graph method.
        If process i is waiting for resource held by process j, add edge i -> j.
        Deadlock exists if there's a cycle.
        """
        wait_for: list[list[int]] = [[] for _ in range(state.num_processes)]

        for i in range(state.num_processes):
            for j in range(state.num_resources):
                if state.max_demand[i][j] > state.allocated[i][j]:
                    for k in range(state.num_processes):
                        if i != k and state.allocated[k][j] > 0:
                            wait_for[i].append(k)

        def has_cycle() -> tuple[bool, set[int]]:
            visited = [False] * state.num_processes
            rec_stack = [False] * state.num_processes
            deadlocked: set[int] = set()

            def dfs(node: int) -> bool:
                visited[node] = True
                rec_stack[node] = True

                for neighbor in wait_for[node]:
                    if not visited[neighbor] and dfs(neighbor):
                        deadlocked.add(node)
                        return True
                    if rec_stack[neighbor]:
                        deadlocked.update({node, neighbor})
                        return True

                rec_stack[node] = False
                return False

            for process_index in range(state.num_processes):
                if not visited[process_index] and dfs(process_index):
                    return True, deadlocked

            return False, deadlocked

        is_deadlock, deadlocked_procs = has_cycle()
        need = DeadlockDetector._build_need_matrix(state)

        if is_deadlock:
            return DeadlockDetectionResult(
                is_deadlock=True,
                deadlocked_processes=deadlocked_procs,
                safe_sequence=None,
                need_matrix=need,
                reason=f"Deadlock detected via Wait-for Graph! Processes {deadlocked_procs} form a cycle.",
            )

        return DeadlockDetectionResult(
            is_deadlock=False,
            deadlocked_processes=set(),
            safe_sequence=list(range(state.num_processes)),
            need_matrix=need,
            reason="No deadlock detected. Wait-for graph has no cycles.",
        )
