"""Deadlock Detection View."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from os_algorithms.deadlock_detection import DeadlockDetector, ResourceAllocationState
from ui.styles import Theme


class DeadlockDetectionView(ttk.Frame):
    """Interactive Deadlock Detection Simulator."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        on_back: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, style="App.TFrame", **kwargs)
        self._on_back = on_back
        self._processes_count = 0
        self._resources_count = 0
        self._allocated = []
        self._max_demand = []
        self._available = []
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

        ttk.Label(header, text="Deadlock Detection Simulator", style="Title.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Analyze resource allocation for deadlock conditions",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        # Main content
        main = ttk.Frame(self, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        # System setup
        setup_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        setup_card.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(setup_card, text="System Configuration", style="CardTitle.TLabel").pack(
            anchor=tk.W
        )

        setup_frame = ttk.Frame(setup_card, style="Card.TFrame")
        setup_frame.pack(fill=tk.X, pady=8)

        ttk.Label(setup_frame, text="Processes:", style="Card.TLabel").pack(side=tk.LEFT, padx=4)
        self.processes_spin = ttk.Spinbox(setup_frame, from_=1, to=10, width=5)
        self.processes_spin.set(3)
        self.processes_spin.pack(side=tk.LEFT, padx=4)

        ttk.Label(setup_frame, text="Resources:", style="Card.TLabel").pack(side=tk.LEFT, padx=4)
        self.resources_spin = ttk.Spinbox(setup_frame, from_=1, to=10, width=5)
        self.resources_spin.set(3)
        self.resources_spin.pack(side=tk.LEFT, padx=4)

        ttk.Button(
            setup_frame,
            text="Setup System",
            style="Accent.TButton",
            command=self._setup_system,
        ).pack(side=tk.LEFT, padx=4)

        # Input matrices
        input_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        input_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        ttk.Label(input_card, text="Resource Allocation Matrices", style="CardTitle.TLabel").pack(
            anchor=tk.W
        )

        # Allocated Resources
        ttk.Label(input_card, text="Allocated Resources:", style="Muted.TLabel").pack(
            anchor=tk.W, pady=(8, 4)
        )
        self.allocated_frame = ttk.Frame(input_card, style="Card.TFrame")
        self.allocated_frame.pack(fill=tk.X, padx=8, pady=4)

        # Max Demand
        ttk.Label(input_card, text="Max Demand:", style="Muted.TLabel").pack(
            anchor=tk.W, pady=(8, 4)
        )
        self.max_frame = ttk.Frame(input_card, style="Card.TFrame")
        self.max_frame.pack(fill=tk.X, padx=8, pady=4)

        # Available Resources
        ttk.Label(input_card, text="Available Resources:", style="Muted.TLabel").pack(
            anchor=tk.W, pady=(8, 4)
        )
        available_frame = ttk.Frame(input_card, style="Card.TFrame")
        available_frame.pack(fill=tk.X, padx=8, pady=4)

        ttk.Label(
            available_frame, text="(Enter space-separated values)", style="Muted.TLabel"
        ).pack(anchor=tk.W)

        self.available_entry = ttk.Entry(available_frame, width=40)
        self.available_entry.pack(fill=tk.X, pady=4)

        # Detection method
        method_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        method_card.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(method_card, text="Detection Method", style="CardTitle.TLabel").pack(anchor=tk.W)

        method_frame = ttk.Frame(method_card, style="Card.TFrame")
        method_frame.pack(fill=tk.X, pady=8)

        self.method_var = tk.StringVar(value="Bankers")

        ttk.Radiobutton(
            method_frame,
            text="Banker's Algorithm",
            variable=self.method_var,
            value="Bankers",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(
            method_frame,
            text="Wait-for Graph",
            variable=self.method_var,
            value="WaitForGraph",
            style="TRadiobutton",
        ).pack(side=tk.LEFT, padx=4)

        # Analyze button
        ttk.Button(
            method_card,
            text="Analyze for Deadlock",
            style="Accent.TButton",
            command=self._analyze,
        ).pack(fill=tk.X, pady=8)

        # Results
        results_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        results_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        ttk.Label(results_card, text="Analysis Results", style="CardTitle.TLabel").pack(anchor=tk.W)

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



    def _setup_system(self) -> None:
        """Setup the system with specified processes and resources."""
        try:
            self._processes_count = int(self.processes_spin.get())
            self._resources_count = int(self.resources_spin.get())

            # Clear existing widgets
            for widget in self.allocated_frame.winfo_children():
                widget.destroy()
            for widget in self.max_frame.winfo_children():
                widget.destroy()

            # Create entry widgets for allocated matrix
            self.allocated_entries = []
            for i in range(self._processes_count):
                row_entries = []
                for j in range(self._resources_count):
                    entry = ttk.Entry(self.allocated_frame, width=5)
                    entry.grid(row=i, column=j, padx=4, pady=2)
                    entry.insert(0, "0")
                    row_entries.append(entry)
                self.allocated_entries.append(row_entries)

            # Create entry widgets for max demand matrix
            self.max_entries = []
            for i in range(self._processes_count):
                row_entries = []
                for j in range(self._resources_count):
                    entry = ttk.Entry(self.max_frame, width=5)
                    entry.grid(row=i, column=j, padx=4, pady=2)
                    entry.insert(0, "0")
                    row_entries.append(entry)
                self.max_entries.append(row_entries)

            # Set placeholder for available resources
            self.available_entry.delete(0, tk.END)
            self.available_entry.insert(
                0, " ".join(["0"] * self._resources_count)
            )

            messagebox.showinfo("System Setup", f"Configured for {self._processes_count} processes and {self._resources_count} resources.\nFill in the matrices with resource values.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def _analyze(self) -> None:
        """Analyze the system for deadlock."""
        if self._processes_count == 0 or self._resources_count == 0:
            messagebox.showwarning("System Not Setup", "Please setup the system first.")
            return

        try:
            # Read allocated matrix
            allocated = []
            for row in self.allocated_entries:
                allocated.append([int(entry.get()) for entry in row])

            # Read max demand matrix
            max_demand = []
            for row in self.max_entries:
                max_demand.append([int(entry.get()) for entry in row])

            # Read available resources
            available = [int(x) for x in self.available_entry.get().strip().split()]

            if len(available) != self._resources_count:
                messagebox.showerror(
                    "Invalid Available Resources",
                    f"Please enter {self._resources_count} values for available resources.",
                )
                return

            # Create state
            state = ResourceAllocationState(
                num_processes=self._processes_count,
                num_resources=self._resources_count,
                allocated=allocated,
                max_demand=max_demand,
                available=available,
            )

            # Run analysis
            method = self.method_var.get()

            if method == "Bankers":
                result = DeadlockDetector.detect_deadlock_bankers(state)
            else:
                result = DeadlockDetector.detect_deadlock_wait_for_graph(state)

            # Display results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)

            output = f"Detection Method: {method}\n"
            output += "=" * 70 + "\n\n"

            if result.is_deadlock:
                output += f"⚠️  DEADLOCK DETECTED!\n"
                output += f"Deadlocked Processes: {sorted(result.deadlocked_processes)}\n"
                output += f"\nReason: {result.reason}\n"
            else:
                output += f"✓ NO DEADLOCK DETECTED\n\n"
                output += f"Reason: {result.reason}\n"
                if result.safe_sequence:
                    output += f"\nSafe Sequence: {[f'P{i}' for i in result.safe_sequence]}\n"

            output += f"\n{'=' * 70}\n"
            output += "Need Matrix (Max - Allocated):\n"
            for i, row in enumerate(result.need_matrix):
                output += f"  P{i}: {row}\n"

            self.results_text.insert(tk.END, output)
            self.results_text.config(state=tk.DISABLED)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid numbers: {str(e)}")
        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred: {str(e)}")
