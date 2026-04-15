"""Registration screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from ui.styles import Theme


class RegisterView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        on_register: Callable[[str, str], None],
        on_back: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, style="App.TFrame", **kwargs)
        self._on_register = on_register
        self._on_back = on_back
        self._error_var = tk.StringVar(value="")
        self._build()

    def _build(self) -> None:
        outer = ttk.Frame(self, style="App.TFrame")
        outer.pack(expand=True, fill=tk.BOTH, padx=40, pady=32)

        ttk.Label(outer, text="Create Account", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            outer,
            text="Strong password required (upper, lower, digit, special).",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 24))

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.pack(fill=tk.X)

        ttk.Label(card, text="Username", style="Card.TLabel").pack(anchor=tk.W)
        self._user = tk.StringVar()
        ttk.Entry(card, textvariable=self._user, width=40).pack(fill=tk.X, pady=(4, 12))

        ttk.Label(card, text="Password", style="Card.TLabel").pack(anchor=tk.W)
        self._pwd = tk.StringVar()
        ttk.Entry(card, textvariable=self._pwd, show="•", width=40).pack(fill=tk.X, pady=(4, 12))

        ttk.Label(card, text="Confirm password", style="Card.TLabel").pack(anchor=tk.W)
        self._pwd2 = tk.StringVar()
        ttk.Entry(card, textvariable=self._pwd2, show="•", width=40).pack(fill=tk.X, pady=(4, 16))

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
        ttk.Button(row, text="Register", style="Accent.TButton", command=self._submit).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(row, text="← Back to Login", style="Ghost.TButton", command=self._on_back).pack(
            side=tk.LEFT
        )

    def _submit(self) -> None:
        self.clear_error()
        if self._pwd.get() != self._pwd2.get():
            self.set_error("Passwords do not match.")
            return
        self._on_register(self._user.get(), self._pwd.get())

    def set_error(self, message: str) -> None:
        self._error_var.set(message)

    def clear_error(self) -> None:
        self._error_var.set("")

    def clear_fields(self) -> None:
        self._user.set("")
        self._pwd.set("")
        self._pwd2.set("")
