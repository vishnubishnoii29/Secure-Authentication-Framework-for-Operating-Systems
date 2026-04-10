"""CPU Scheduling Algorithms - FCFS, SJF, RR, Priority Scheduling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Process:
    """Represents a process with arrival time, burst time, and priority."""

    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0

    def __repr__(self) -> str:
        return f"P{self.pid}"


@dataclass
class SchedulingResult:
    """Stores scheduling algorithm result."""

    algorithm_name: str
    gantt_chart: List[tuple[str, int, int]]  # (process_name, start_time, end_time)
    waiting_times: dict[int, int]  # process_id: waiting_time
    turnaround_times: dict[int, int]  # process_id: turnaround_time
    avg_waiting_time: float
    avg_turnaround_time: float


class CPUScheduler:
    """CPU Scheduling algorithms implementation."""

    @staticmethod
    def fcfs(processes: List[Process]) -> SchedulingResult:
        """First Come First Serve scheduling."""
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart = []
        waiting_times = {}
        turnaround_times = {}
        current_time = 0

        for process in sorted_processes:
            start_time = max(current_time, process.arrival_time)
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))

            waiting_time = start_time - process.arrival_time
            turnaround_time = end_time - process.arrival_time

            waiting_times[process.pid] = waiting_time
            turnaround_times[process.pid] = turnaround_time

            current_time = end_time

        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)

        return SchedulingResult(
            algorithm_name="FCFS (First Come First Serve)",
            gantt_chart=gantt_chart,
            waiting_times=waiting_times,
            turnaround_times=turnaround_times,
            avg_waiting_time=avg_waiting,
            avg_turnaround_time=avg_turnaround,
        )

    @staticmethod
    def sjf(processes: List[Process]) -> SchedulingResult:
        """Shortest Job First scheduling (non-preemptive)."""
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart = []
        waiting_times = {}
        turnaround_times = {}
        current_time = 0
        remaining = list(sorted_processes)

        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p.arrival_time <= current_time]

            if not available:
                # No process available, jump to next arrival
                current_time = min(p.arrival_time for p in remaining)
                continue

            # Select shortest burst time
            process = min(available, key=lambda p: p.burst_time)
            start_time = current_time
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))

            waiting_time = start_time - process.arrival_time
            turnaround_time = end_time - process.arrival_time

            waiting_times[process.pid] = waiting_time
            turnaround_times[process.pid] = turnaround_time

            remaining.remove(process)
            current_time = end_time

        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)

        return SchedulingResult(
            algorithm_name="SJF (Shortest Job First)",
            gantt_chart=gantt_chart,
            waiting_times=waiting_times,
            turnaround_times=turnaround_times,
            avg_waiting_time=avg_waiting,
            avg_turnaround_time=avg_turnaround,
        )

    @staticmethod
    def round_robin(processes: List[Process], time_quantum: int) -> SchedulingResult:
        """Round Robin scheduling with time quantum."""
        from collections import deque

        queue = deque()
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart = []
        waiting_times = {p.pid: 0 for p in processes}
        turnaround_times = {}
        current_time = 0
        remaining_bursts = {p.pid: p.burst_time for p in processes}
        completed = set()

        # Add initial processes
        for p in sorted_processes:
            if p.arrival_time <= current_time:
                queue.append(p)

        while queue or any(p.arrival_time > current_time for p in sorted_processes):
            if not queue:
                # Jump to next arrival
                current_time = min(
                    p.arrival_time
                    for p in sorted_processes
                    if p not in completed and p.arrival_time > current_time
                )
                for p in sorted_processes:
                    if p.arrival_time <= current_time and p not in queue and p not in completed:
                        queue.append(p)
                continue

            process = queue.popleft()
            start_time = current_time
            time_slice = min(time_quantum, remaining_bursts[process.pid])
            end_time = start_time + time_slice
            gantt_chart.append((str(process), start_time, end_time))

            remaining_bursts[process.pid] -= time_slice
            current_time = end_time

            # Add newly arrived processes
            for p in sorted_processes:
                if p.arrival_time <= current_time and p not in queue and p not in completed:
                    queue.append(p)

            if remaining_bursts[process.pid] > 0:
                queue.append(process)
            else:
                completed.add(process)
                turnaround_times[process.pid] = end_time - process.arrival_time

        # Calculate waiting times
        for process in processes:
            waiting_times[process.pid] = turnaround_times[process.pid] - process.burst_time

        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)

        return SchedulingResult(
            algorithm_name=f"Round Robin (Quantum={time_quantum})",
            gantt_chart=gantt_chart,
            waiting_times=waiting_times,
            turnaround_times=turnaround_times,
            avg_waiting_time=avg_waiting,
            avg_turnaround_time=avg_turnaround,
        )

    @staticmethod
    def priority_scheduling(processes: List[Process]) -> SchedulingResult:
        """Priority Scheduling (non-preemptive, lower priority number = higher priority)."""
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart = []
        waiting_times = {}
        turnaround_times = {}
        current_time = 0
        remaining = list(sorted_processes)

        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p.arrival_time <= current_time]

            if not available:
                # No process available, jump to next arrival
                current_time = min(p.arrival_time for p in remaining)
                continue

            # Select highest priority (lowest priority number)
            process = min(available, key=lambda p: p.priority)
            start_time = current_time
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))

            waiting_time = start_time - process.arrival_time
            turnaround_time = end_time - process.arrival_time

            waiting_times[process.pid] = waiting_time
            turnaround_times[process.pid] = turnaround_time

            remaining.remove(process)
            current_time = end_time

        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)

        return SchedulingResult(
            algorithm_name="Priority Scheduling",
            gantt_chart=gantt_chart,
            waiting_times=waiting_times,
            turnaround_times=turnaround_times,
            avg_waiting_time=avg_waiting,
            avg_turnaround_time=avg_turnaround,
        )
