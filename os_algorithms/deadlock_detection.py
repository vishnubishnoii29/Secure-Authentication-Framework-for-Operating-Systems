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
    def detect_deadlock_bankers(state: ResourceAllocationState) -> DeadlockDetectionResult:
        """
        Detect deadlock using Banker's Algorithm.
        Returns safe sequence if exists, otherwise indicates deadlock.
        """
        # Calculate need matrix: Need[i][j] = Max[i][j] - Allocated[i][j]
        need = []
        for i in range(state.num_processes):
            need.append([])
            for j in range(state.num_resources):
                need[i].append(state.max_demand[i][j] - state.allocated[i][j])

        # Try to find a safe sequence
        work = list(state.available)
        finish = [False] * state.num_processes
        safe_sequence = []

        for _ in range(state.num_processes):
            found = False

            for i in range(state.num_processes):
                if finish[i]:
                    continue

                # Check if process i can be satisfied with current resources
                can_satisfy = True
                for j in range(state.num_resources):
                    if need[i][j] > work[j]:
                        can_satisfy = False
                        break

                if can_satisfy:
                    # Process i can be satisfied
                    safe_sequence.append(i)
                    finish[i] = True

                    # Release resources
                    for j in range(state.num_resources):
                        work[j] += state.allocated[i][j]

                    found = True
                    break

            if not found:
                # No process can be satisfied, deadlock detected
                deadlocked = {i for i in range(state.num_processes) if not finish[i]}
                return DeadlockDetectionResult(
                    is_deadlock=True,
                    deadlocked_processes=deadlocked,
                    safe_sequence=None,
                    need_matrix=need,
                    reason=f"Deadlock detected! Processes {deadlocked} are stuck.",
                )

        # All processes can be satisfied, system is safe
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
        # Build wait-for graph
        wait_for = [[] for _ in range(state.num_processes)]

        for i in range(state.num_processes):
            for j in range(state.num_resources):
                # If process i needs resource j but doesn't have it
                if state.max_demand[i][j] > state.allocated[i][j]:
                    # Find which process holds this resource
                    for k in range(state.num_processes):
                        if i != k and state.allocated[k][j] > 0:
                            wait_for[i].append(k)

        # Detect cycle using DFS
        def has_cycle() -> tuple[bool, Set[int]]:
            visited = [False] * state.num_processes
            rec_stack = [False] * state.num_processes
            deadlocked = set()

            def dfs(node: int) -> bool:
                visited[node] = True
                rec_stack[node] = True

                for neighbor in wait_for[node]:
                    if not visited[neighbor]:
                        if dfs(neighbor):
                            deadlocked.add(node)
                            return True
                    elif rec_stack[neighbor]:
                        deadlocked.add(node)
                        deadlocked.add(neighbor)
                        return True

                rec_stack[node] = False
                return False

            for i in range(state.num_processes):
                if not visited[i]:
                    if dfs(i):
                        return True, deadlocked

            return False, deadlocked

        is_deadlock, deadlocked_procs = has_cycle()

        # Calculate need matrix
        need = []
        for i in range(state.num_processes):
            need.append([])
            for j in range(state.num_resources):
                need[i].append(state.max_demand[i][j] - state.allocated[i][j])

        if is_deadlock:
            return DeadlockDetectionResult(
                is_deadlock=True,
                deadlocked_processes=deadlocked_procs,
                safe_sequence=None,
                need_matrix=need,
                reason=f"Deadlock detected via Wait-for Graph! Processes {deadlocked_procs} form a cycle.",
            )
        else:
            return DeadlockDetectionResult(
                is_deadlock=False,
                deadlocked_processes=set(),
                safe_sequence=list(range(state.num_processes)),
                need_matrix=need,
                reason="No deadlock detected. Wait-for graph has no cycles.",
            )
