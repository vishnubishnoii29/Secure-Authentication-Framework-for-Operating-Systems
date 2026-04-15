"""CPU Scheduling Simulator View."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from os_algorithms.cpu_scheduling import CPUScheduler, Process
from ui.styles import Theme


class CPUSchedulingView(ttk.Frame):
    """Interactive CPU Scheduling Simulator."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        on_back: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, style="App.TFrame", **kwargs)
        self._on_back = on_back
        self._processes = []
        self._build()

    def _build(self) -> None:
        # Top Header with Back Button
        top_header = ttk.Frame(self, style="App.TFrame")
        top_header.pack(fill=tk.X, padx=20, pady=(12, 0))
        
        ttk.Button(top_header, text="← Back to Dashboard", style="Ghost.TButton", command=self._on_back).pack(
            anchor=tk.W
        )
        
        # Header
        header = ttk.Frame(self, style="App.TFrame")
        header.pack(fill=tk.X, padx=20, pady=(12, 16))

        ttk.Label(header, text="CPU Scheduling Simulator", style="Title.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header, text="Compare different scheduling algorithms", style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(4, 0))

        # Main content
        main = ttk.Frame(self, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        # Input section
        input_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        input_card.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(input_card, text="Add Process", style="CardTitle.TLabel").pack(anchor=tk.W)

        input_frame = ttk.Frame(input_card, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=8)

        ttk.Label(input_frame, text="Arrival:", style="Card.TLabel").pack(side=tk.LEFT, padx=4)
        self.arrival_entry = ttk.Entry(input_frame, width=8)
        self.arrival_entry.pack(side=tk.LEFT, padx=4)

        ttk.Label(input_frame, text="Burst:", style="Card.TLabel").pack(side=tk.LEFT, padx=4)
        self.burst_entry = ttk.Entry(input_frame, width=8)
        self.burst_entry.pack(side=tk.LEFT, padx=4)

        ttk.Label(input_frame, text="Priority:", style="Card.TLabel").pack(side=tk.LEFT, padx=4)
        self.priority_entry = ttk.Entry(input_frame, width=8)
        self.priority_entry.pack(side=tk.LEFT, padx=4)

        ttk.Button(
            input_frame, text="Add", style="Accent.TButton", command=self._add_process
        ).pack(side=tk.LEFT, padx=4)

        # Process list
        list_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        list_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        ttk.Label(list_card, text="Processes", style="CardTitle.TLabel").pack(anchor=tk.W)

        self.process_listbox = tk.Listbox(
            list_card,
            bg=Theme.FIELD_BG,
            fg=Theme.FG,
            selectmode=tk.SINGLE,
            height=6,
            font=("Consolas", 9),
            relief=tk.FLAT,
        )
        self.process_listbox.pack(fill=tk.BOTH, expand=True, pady=8)

        btn_frame = ttk.Frame(list_card, style="Card.TFrame")
        btn_frame.pack(fill=tk.X)
        ttk.Button(
            btn_frame, text="Remove Selected", style="Ghost.TButton", command=self._remove_process
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Clear All", style="Ghost.TButton", command=self._clear_all).pack(
            side=tk.LEFT, padx=4
        )

        # Scheduling options
        options_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        options_card.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(options_card, text="Select Algorithm", style="CardTitle.TLabel").pack(
            anchor=tk.W
        )

        algo_frame = ttk.Frame(options_card, style="Card.TFrame")
        algo_frame.pack(fill=tk.X, pady=8)

        self.time_quantum = ttk.Entry(algo_frame, width=5)
        self.algorithm_var = tk.StringVar(value="FCFS")

        ttk.Radiobutton(
            algo_frame,
            text="FCFS",
            variable=self.algorithm_var,
            value="FCFS",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(
            algo_frame,
            text="SJF",
            variable=self.algorithm_var,
            value="SJF",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(
            algo_frame,
            text="Round Robin (Quantum:",
            variable=self.algorithm_var,
            value="RR",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)
        self.time_quantum.pack(side=tk.LEFT, padx=0)
        ttk.Label(algo_frame, text=")", style="Card.TLabel").pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(
            algo_frame,
            text="Priority",
            variable=self.algorithm_var,
            value="Priority",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)

        # Run button
        ttk.Button(
            options_card,
            text="Calculate & View Results",
            style="Accent.TButton",
            command=self._calculate,
        ).pack(fill=tk.X, pady=8)

        # Results section
        results_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        results_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        ttk.Label(results_card, text="Results", style="CardTitle.TLabel").pack(anchor=tk.W)

        self.results_text = tk.Text(
            results_card,
            height=10,
            wrap=tk.WORD,
            bg=Theme.FIELD_BG,
            fg=Theme.FG,
            insertbackground=Theme.FG,
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)



    def _add_process(self) -> None:
        """Add a new process."""
        try:
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())

            if arrival < 0 or burst <= 0 or priority < 0:
                messagebox.showerror("Invalid Input", "Please enter valid positive numbers.")
                return

            pid = len(self._processes)
            process = Process(
                pid=pid, arrival_time=arrival, burst_time=burst, priority=priority
            )
            self._processes.append(process)

            self.process_listbox.insert(
                tk.END,
                f"P{pid}: Arrival={arrival}, Burst={burst}, Priority={priority}",
            )

            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.arrival_entry.focus()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values.")

    def _remove_process(self) -> None:
        """Remove selected process."""
        selection = self.process_listbox.curselection()
        if selection:
            idx = selection[0]
            self.process_listbox.delete(idx)
            del self._processes[idx]
            # Reassign PIDs
            for i, p in enumerate(self._processes):
                p.pid = i
                self._update_process_display(i)

    def _clear_all(self) -> None:
        """Clear all processes."""
        self.process_listbox.delete(0, tk.END)
        self._processes = []
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)

    def _update_process_display(self, idx: int) -> None:
        """Update display for a process."""
        p = self._processes[idx]
        self.process_listbox.delete(idx)
        self.process_listbox.insert(
            idx,
            f"P{p.pid}: Arrival={p.arrival_time}, Burst={p.burst_time}, Priority={p.priority}",
        )

    def _calculate(self) -> None:
        """Calculate scheduling results."""
        if not self._processes:
            messagebox.showwarning("No Processes", "Please add at least one process.")
            return

        algorithm = self.algorithm_var.get()

        try:
            if algorithm == "FCFS":
                result = CPUScheduler.fcfs(self._processes)
            elif algorithm == "SJF":
                result = CPUScheduler.sjf(self._processes)
            elif algorithm == "RR":
                try:
                    quantum = int(self.time_quantum.get())
                    if quantum <= 0:
                        raise ValueError("Quantum must be positive")
                except ValueError:
                    messagebox.showerror("Invalid Quantum", "Please enter a valid time quantum.")
                    return
                result = CPUScheduler.round_robin(self._processes, quantum)
            elif algorithm == "Priority":
                result = CPUScheduler.priority_scheduling(self._processes)
            else:
                return

            # Display results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)

            output = f"Algorithm: {result.algorithm_name}\n"
            output += "=" * 70 + "\n\n"

            output += "Gantt Chart:\n"
            for proc_name, start, end in result.gantt_chart:
                output += f"  {proc_name}: {start} → {end} (Duration: {end - start})\n"

            output += f"\nWaiting Times:\n"
            for pid, wt in result.waiting_times.items():
                output += f"  P{pid}: {wt}\n"

            output += f"\nTurnaround Times:\n"
            for pid, tt in result.turnaround_times.items():
                output += f"  P{pid}: {tt}\n"

            output += f"\n{'=' * 70}\n"
            output += f"Average Waiting Time: {result.avg_waiting_time:.2f}\n"
            output += f"Average Turnaround Time: {result.avg_turnaround_time:.2f}\n"

            self.results_text.insert(tk.END, output)
            self.results_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
