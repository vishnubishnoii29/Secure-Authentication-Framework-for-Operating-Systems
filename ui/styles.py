"""Tkinter / ttk styling for a modern dashboard look."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class Theme:
    # Base colors
    BG = "#0f1419"
    BG_ELEVATED = "#1a2332"
    BG_HOVER = "#232f42"
    FG = "#e7ecf3"
    FG_MUTED = "#8b9bb4"
    
    # Accent colors
    ACCENT = "#3d9cf0"
    ACCENT_HOVER = "#5cb0ff"
    ACCENT_LIGHT = "#5cb0ff"
    
    # Status colors
    SUCCESS = "#3dd68c"
    SUCCESS_HOVER = "#4fe99d"
    ERROR = "#f07178"
    ERROR_HOVER = "#f89a9e"
    WARNING = "#ffb454"
    WARNING_HOVER = "#ffc670"
    
    # Utility colors
    BORDER = "#2d3a4f"
    FIELD_BG = "#131b26"
    FIELD_FOCUS = "#1e2b3c"


def apply_root_style(root: tk.Tk) -> None:
    root.configure(bg=Theme.BG)
    # Brace-quoted family: required for Tcl 9 / Python 3.14+ multi-word font names
    root.option_add("*Font", "{Segoe UI} 10")
    root.option_add("*TLabel*background", Theme.BG)
    root.option_add("*TLabel*foreground", Theme.FG)


def configure_ttk_styles() -> ttk.Style:
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Frame styles
    style.configure(
        "App.TFrame",
        background=Theme.BG,
    )
    style.configure(
        "Card.TFrame",
        background=Theme.BG_ELEVATED,
        relief="flat",
    )
    
    # Label styles
    style.configure(
        "Title.TLabel",
        background=Theme.BG,
        foreground=Theme.FG,
        font="{Segoe UI} 22 bold",
    )
    style.configure(
        "Subtitle.TLabel",
        background=Theme.BG,
        foreground=Theme.FG_MUTED,
        font="{Segoe UI} 11",
    )
    style.configure(
        "Muted.TLabel",
        background=Theme.BG_ELEVATED,
        foreground=Theme.FG_MUTED,
        font="{Segoe UI} 9",
    )
    style.configure(
        "Card.TLabel",
        background=Theme.BG_ELEVATED,
        foreground=Theme.FG,
        font="{Segoe UI} 10",
    )
    style.configure(
        "CardTitle.TLabel",
        background=Theme.BG_ELEVATED,
        foreground=Theme.FG,
        font="{Segoe UI} 14 bold",
    )
    style.configure(
        "TLabel",
        background=Theme.BG,
        foreground=Theme.FG,
    )
    style.configure(
        "Link.TLabel",
        background=Theme.BG,
        foreground=Theme.ACCENT,
        font="{Segoe UI} 10 underline",
    )
    
    # Entry styles
    style.configure(
        "TEntry",
        fieldbackground=Theme.FIELD_BG,
        foreground=Theme.FG,
        insertcolor=Theme.FG,
        padding=8,
        relief="flat",
        borderwidth=1,
    )
    style.map(
        "TEntry",
        fieldbackground=[
            ("readonly", Theme.FIELD_BG),
            ("focus", Theme.FIELD_FOCUS),
        ],
        foreground=[("disabled", Theme.FG_MUTED)],
    )
    
    # Primary button (Accent)
    style.configure(
        "Accent.TButton",
        background=Theme.ACCENT,
        foreground="#ffffff",
        font="{Segoe UI} 10 bold",
        padding=(16, 10),
        borderwidth=0,
        focuscolor=Theme.ACCENT,
        relief="flat",
    )
    style.map(
        "Accent.TButton",
        background=[
            ("active", Theme.ACCENT_HOVER),
            ("pressed", Theme.ACCENT_HOVER),
            ("disabled", "#3a4f66"),
        ],
        foreground=[("disabled", "#8899aa")],
    )
    
    # Secondary button (Ghost)
    style.configure(
        "Ghost.TButton",
        background=Theme.BG_ELEVATED,
        foreground=Theme.FG,
        font="{Segoe UI} 10",
        padding=(12, 8),
        borderwidth=1,
        relief="flat",
    )
    style.map(
        "Ghost.TButton",
        background=[
            ("active", Theme.BG_HOVER),
            ("pressed", Theme.BG_HOVER),
        ],
        foreground=[("disabled", Theme.FG_MUTED)],
    )
    
    # Success button
    style.configure(
        "Success.TButton",
        background=Theme.SUCCESS,
        foreground="#ffffff",
        font="{Segoe UI} 10 bold",
        padding=(16, 10),
        borderwidth=0,
        focuscolor=Theme.SUCCESS,
        relief="flat",
    )
    style.map(
        "Success.TButton",
        background=[
            ("active", Theme.SUCCESS_HOVER),
            ("pressed", Theme.SUCCESS_HOVER),
            ("disabled", "#2d5c5c"),
        ],
        foreground=[("disabled", "#8899aa")],
    )
    
    # Radio and Check buttons with better styling
    style.map(
        "TRadiobutton",
        background=[("active", Theme.BG_ELEVATED)],
        foreground=[("active", Theme.FG)],
    )
    style.map(
        "TCheckbutton",
        background=[("active", Theme.BG_ELEVATED)],
        foreground=[("active", Theme.FG)],
    )
    
    # Spinbox styling
    style.configure(
        "TSpinbox",
        fieldbackground=Theme.FIELD_BG,
        foreground=Theme.FG,
        insertcolor=Theme.FG,
        padding=6,
        relief="flat",
        borderwidth=1,
    )
    
    # Scrollbar styling
    style.configure(
        "Vertical.TScrollbar",
        background=Theme.BG,
        troughcolor=Theme.BG_ELEVATED,
        bordercolor=Theme.BORDER,
        arrowcolor=Theme.FG_MUTED,
        darkcolor=Theme.BG_ELEVATED,
        lightcolor=Theme.BG_ELEVATED,
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", Theme.ACCENT)],
    )
    
    return style

