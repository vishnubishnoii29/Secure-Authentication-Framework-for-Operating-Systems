"""Post-login dashboard."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from auth.service import SessionState
from ui.styles import Theme


class DashboardView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        on_logout: Callable[[], None],
        on_cpu_scheduling: Callable[[], None],
        on_deadlock_detection: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, style="App.TFrame", **kwargs)
        self._on_logout = on_logout
        self._on_cpu_scheduling = on_cpu_scheduling
        self._on_deadlock_detection = on_deadlock_detection
        self._welcome = tk.StringVar()
        self._meta = tk.StringVar()
        self._build()

    def _build(self) -> None:
        # Create scrollable area
        canvas = tk.Canvas(self, bg=Theme.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="App.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        outer = ttk.Frame(scrollable_frame, style="App.TFrame")
        outer.pack(expand=True, fill=tk.BOTH, padx=20, pady=16)

        # Header
        ttk.Label(outer, text="Dashboard", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(outer, textvariable=self._welcome, style="Subtitle.TLabel").pack(
            anchor=tk.W, pady=(8, 4)
        )
        ttk.Label(outer, textvariable=self._meta, style="Subtitle.TLabel").pack(anchor=tk.W)

        # Session Security Card
        session_card = ttk.Frame(outer, style="Card.TFrame", padding=20)
        session_card.pack(fill=tk.X, pady=(16, 12))

        ttk.Label(session_card, text="Session Security (Demo)", style="CardTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            session_card,
            text="Integrity token (generated at login, stored encrypted in memory):",
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(8, 4))

        tok = tk.Text(
            session_card,
            height=2,
            wrap=tk.WORD,
            bg=Theme.FIELD_BG,
            fg=Theme.FG,
            insertbackground=Theme.FG,
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        tok.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        self._token_widget = tok

        session_btn_frame = ttk.Frame(session_card, style="Card.TFrame")
        session_btn_frame.pack(fill=tk.X)
        ttk.Button(
            session_btn_frame, text="Log out", style="Accent.TButton", command=self._on_logout
        ).pack(anchor=tk.W)

        # OS Tools Section
        tools_label = ttk.Label(
            outer, text="Operating System Tools", style="Title.TLabel"
        )
        tools_label.pack(anchor=tk.W, pady=(20, 12))

        # CPU Scheduling Card
        cpu_card = ttk.Frame(outer, style="Card.TFrame", padding=20)
        cpu_card.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(cpu_card, text="CPU Scheduling Simulator", style="CardTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            cpu_card,
            text="Analyze different CPU scheduling algorithms (FCFS, SJF, Round Robin, Priority)",
            style="Muted.TLabel",
            wraplength=400,
        ).pack(anchor=tk.W, pady=(4, 12))

        cpu_btn_frame = ttk.Frame(cpu_card, style="Card.TFrame")
        cpu_btn_frame.pack(fill=tk.X)
        ttk.Button(
            cpu_btn_frame,
            text="→ Open CPU Scheduler",
            style="Accent.TButton",
            command=self._on_cpu_scheduling,
        ).pack(anchor=tk.W)

        # Deadlock Detection Card
        deadlock_card = ttk.Frame(outer, style="Card.TFrame", padding=20)
        deadlock_card.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(
            deadlock_card, text="Deadlock Detection Simulator", style="CardTitle.TLabel"
        ).pack(anchor=tk.W)
        ttk.Label(
            deadlock_card,
            text="Detect and analyze deadlock conditions using Banker's Algorithm and Wait-for Graph",
            style="Muted.TLabel",
            wraplength=400,
        ).pack(anchor=tk.W, pady=(4, 12))

        deadlock_btn_frame = ttk.Frame(deadlock_card, style="Card.TFrame")
        deadlock_btn_frame.pack(fill=tk.X)
        ttk.Button(
            deadlock_btn_frame,
            text="→ Open Deadlock Detector",
            style="Accent.TButton",
            command=self._on_deadlock_detection,
        ).pack(anchor=tk.W)

    def set_session(self, session: SessionState) -> None:
        self._welcome.set(f"Welcome, {session.username}.")
        self._meta.set(f"Account ID {session.user_id} · Registered {session.created_at}")
        token = session.session_display_token
        self._token_widget.configure(state=tk.NORMAL)
        self._token_widget.delete("1.0", tk.END)
        self._token_widget.insert(tk.END, token)
        self._token_widget.configure(state=tk.DISABLED)
