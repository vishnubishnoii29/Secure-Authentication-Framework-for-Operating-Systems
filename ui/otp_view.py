"""OTP verification (simulated delivery)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from ui.styles import Theme


class OTPView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        on_verify: Callable[[str], None],
        on_cancel: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, style="App.TFrame", **kwargs)
        self._on_verify = on_verify
        self._on_cancel = on_cancel
        self._error_var = tk.StringVar(value="")
        self._simulated_var = tk.StringVar(value="")
        self._build()

    def _build(self) -> None:
        outer = ttk.Frame(self, style="App.TFrame")
        outer.pack(expand=True, fill=tk.BOTH, padx=40, pady=32)

        ttk.Label(outer, text="Two-Factor Verification", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            outer,
            text="Simulated OTP (demo): shown below as if delivered to your device.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 24))

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.pack(fill=tk.X)

        ttk.Label(card, text="Simulated OTP", style="CardTitle.TLabel").pack(anchor=tk.W)
        sim = tk.Label(
            card,
            textvariable=self._simulated_var,
            fg=Theme.SUCCESS,
            bg=Theme.BG_ELEVATED,
            font=("Consolas", 18, "bold"),
            pady=8,
        )
        sim.pack(anchor=tk.W, pady=(8, 16))

        ttk.Label(card, text="Enter OTP", style="Card.TLabel").pack(anchor=tk.W)
        self._otp = tk.StringVar()
        ent = ttk.Entry(card, textvariable=self._otp, width=24)
        ent.pack(fill=tk.X, pady=(4, 16))

        err = tk.Label(
            card,
            textvariable=self._error_var,
            fg=Theme.ERROR,
            bg=Theme.BG_ELEVATED,
            font="{Segoe UI} 9",
            wraplength=360,
            justify=tk.LEFT,
        )
        err.pack(anchor=tk.W, pady=(0, 12))

        row = ttk.Frame(card, style="Card.TFrame")
        row.pack(fill=tk.X)
        ttk.Button(row, text="Verify & sign in", style="Accent.TButton", command=self._submit).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(row, text="← Back to Login", style="Ghost.TButton", command=self._on_cancel).pack(
            side=tk.LEFT
        )

        ent.focus_set()

    def show_challenge(self, username: str, otp_code: str) -> None:
        self._simulated_var.set(f"User: {username}  |  OTP: {otp_code}")
        self._otp.set("")
        self.clear_error()

    def _submit(self) -> None:
        self.clear_error()
        self._on_verify(self._otp.get())

    def set_error(self, message: str) -> None:
        self._error_var.set(message)

    def clear_error(self) -> None:
        self._error_var.set("")

    def clear_simulated(self) -> None:
        self._simulated_var.set("")
        self._otp.set("")
