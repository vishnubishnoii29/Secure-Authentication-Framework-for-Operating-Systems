"""CPU Scheduling Algorithms - FCFS, SJF, RR, Priority Scheduling."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Process:
    """Represents a process with arrival time, burst time, and priority."""

    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0

    def __repr__(self) -> str:
        return f"P{self.pid}"


@dataclass(slots=True)
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
    def _build_result(
        algorithm_name: str,
        gantt_chart: list[tuple[str, int, int]],
        waiting_times: dict[int, int],
        turnaround_times: dict[int, int],
    ) -> SchedulingResult:
        if not waiting_times or not turnaround_times:
            raise ValueError("Scheduling requires at least one process.")
        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)
        return SchedulingResult(
            algorithm_name=algorithm_name,
            gantt_chart=gantt_chart,
            waiting_times=waiting_times,
            turnaround_times=turnaround_times,
            avg_waiting_time=avg_waiting,
            avg_turnaround_time=avg_turnaround,
        )

    @staticmethod
    def fcfs(processes: List[Process]) -> SchedulingResult:
        """First Come First Serve scheduling."""
        if not processes:
            raise ValueError("At least one process is required for FCFS scheduling.")
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart: list[tuple[str, int, int]] = []
        waiting_times: dict[int, int] = {}
        turnaround_times: dict[int, int] = {}
        current_time = 0

        for process in sorted_processes:
            start_time = max(current_time, process.arrival_time)
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))
            waiting_times[process.pid] = start_time - process.arrival_time
            turnaround_times[process.pid] = end_time - process.arrival_time
            current_time = end_time

        return CPUScheduler._build_result(
            "FCFS (First Come First Serve)",
            gantt_chart,
            waiting_times,
            turnaround_times,
        )

    @staticmethod
    def sjf(processes: List[Process]) -> SchedulingResult:
        """Shortest Job First scheduling (non-preemptive)."""
        if not processes:
            raise ValueError("At least one process is required for SJF scheduling.")
        remaining = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart: list[tuple[str, int, int]] = []
        waiting_times: dict[int, int] = {}
        turnaround_times: dict[int, int] = {}
        current_time = 0

        while remaining:
            available = [p for p in remaining if p.arrival_time <= current_time]
            if not available:
                current_time = min(p.arrival_time for p in remaining)
                continue

            process = min(available, key=lambda p: p.burst_time)
            start_time = current_time
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))
            waiting_times[process.pid] = start_time - process.arrival_time
            turnaround_times[process.pid] = end_time - process.arrival_time
            remaining.remove(process)
            current_time = end_time

        return CPUScheduler._build_result(
            "SJF (Shortest Job First)",
            gantt_chart,
            waiting_times,
            turnaround_times,
        )

    @staticmethod
    def round_robin(processes: List[Process], time_quantum: int) -> SchedulingResult:
        """Round Robin scheduling with time quantum."""
        if not processes:
            raise ValueError("At least one process is required for Round Robin scheduling.")
        if time_quantum <= 0:
            raise ValueError("Time quantum must be a positive integer.")
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart: list[tuple[str, int, int]] = []
        waiting_times = {p.pid: 0 for p in sorted_processes}
        turnaround_times: dict[int, int] = {}
        remaining_bursts = {p.pid: p.burst_time for p in sorted_processes}
        queue = deque()
        current_time = 0
        next_index = 0

        while next_index < len(sorted_processes) or queue:
            while next_index < len(sorted_processes) and sorted_processes[next_index].arrival_time <= current_time:
                queue.append(sorted_processes[next_index])
                next_index += 1

            if not queue:
                current_time = sorted_processes[next_index].arrival_time
                continue

            process = queue.popleft()
            time_slice = min(time_quantum, remaining_bursts[process.pid])
            start_time = current_time
            end_time = start_time + time_slice
            gantt_chart.append((str(process), start_time, end_time))
            remaining_bursts[process.pid] -= time_slice
            current_time = end_time

            while next_index < len(sorted_processes) and sorted_processes[next_index].arrival_time <= current_time:
                queue.append(sorted_processes[next_index])
                next_index += 1

            if remaining_bursts[process.pid] > 0:
                queue.append(process)
            else:
                turnaround_times[process.pid] = end_time - process.arrival_time

        for process in sorted_processes:
            waiting_times[process.pid] = turnaround_times[process.pid] - process.burst_time

        return CPUScheduler._build_result(
            f"Round Robin (Quantum={time_quantum})",
            gantt_chart,
            waiting_times,
            turnaround_times,
        )

    @staticmethod
    def priority_scheduling(processes: List[Process]) -> SchedulingResult:
        """Priority Scheduling (non-preemptive, lower priority number = higher priority)."""
        if not processes:
            raise ValueError("At least one process is required for Priority scheduling.")
        remaining = sorted(processes, key=lambda p: p.arrival_time)
        gantt_chart: list[tuple[str, int, int]] = []
        waiting_times: dict[int, int] = {}
        turnaround_times: dict[int, int] = {}
        current_time = 0

        while remaining:
            available = [p for p in remaining if p.arrival_time <= current_time]
            if not available:
                current_time = min(p.arrival_time for p in remaining)
                continue

            process = min(available, key=lambda p: p.priority)
            start_time = current_time
            end_time = start_time + process.burst_time
            gantt_chart.append((str(process), start_time, end_time))
            waiting_times[process.pid] = start_time - process.arrival_time
            turnaround_times[process.pid] = end_time - process.arrival_time
            remaining.remove(process)
            current_time = end_time

        return CPUScheduler._build_result(
            "Priority Scheduling",
            gantt_chart,
            waiting_times,
            turnaround_times,
        )
