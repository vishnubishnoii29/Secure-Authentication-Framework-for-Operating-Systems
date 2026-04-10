"""Main window: screen stack and auth wiring."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from auth.service import AuthError, AuthService
from database.connection import init_database
from logs.logger import get_logger, log_event
from ui.cpu_scheduling_view import CPUSchedulingView
from ui.dashboard_view import DashboardView
from ui.deadlock_detection_view import DeadlockDetectionView
from ui.login_view import LoginView
from ui.otp_view import OTPView
from ui.register_view import RegisterView
from ui.styles import Theme, apply_root_style, configure_ttk_styles


class AuthApplication:
    def __init__(self) -> None:
        init_database()
        get_logger()
        log_event("app_started", detail="framework_boot")

        self._auth = AuthService()
        self.root = tk.Tk()
        self.root.title("Secure Authentication Framework")
        self.root.minsize(640, 480)
        self.root.geometry("900x700")

        apply_root_style(self.root)
        configure_ttk_styles()

        self._container = ttk.Frame(self.root, style="App.TFrame")
        self._container.pack(fill=tk.BOTH, expand=True)

        self._login = LoginView(
            self._container,
            on_login=self._handle_login,
            on_go_register=self._show_register,
        )
        self._register = RegisterView(
            self._container,
            on_register=self._handle_register,
            on_back=self._show_login,
        )
        self._otp = OTPView(
            self._container,
            on_verify=self._handle_otp,
            on_cancel=self._cancel_otp,
        )
        self._dashboard = DashboardView(
            self._container,
            on_logout=self._handle_logout,
            on_cpu_scheduling=self._show_cpu_scheduling,
            on_deadlock_detection=self._show_deadlock_detection,
        )
        self._cpu_scheduling = CPUSchedulingView(
            self._container,
            on_back=self._show_dashboard,
        )
        self._deadlock_detection = DeadlockDetectionView(
            self._container,
            on_back=self._show_dashboard,
        )

        for f in (
            self._login,
            self._register,
            self._otp,
            self._dashboard,
            self._cpu_scheduling,
            self._deadlock_detection,
        ):
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._show_login()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def run(self) -> None:
        self.root.mainloop()

    def _raise(self, frame: tk.Widget) -> None:
        frame.tkraise()

    def _show_login(self) -> None:
        self._auth.cancel_otp()
        self._login.clear_error()
        self._raise(self._login)

    def _show_register(self) -> None:
        self._register.clear_error()
        self._raise(self._register)

    def _show_otp(self, username: str, code: str) -> None:
        self._otp.show_challenge(username, code)
        self._raise(self._otp)

    def _show_dashboard(self) -> None:
        session = self._auth.session
        if session:
            self._dashboard.set_session(session)
        self._raise(self._dashboard)

    def _show_cpu_scheduling(self) -> None:
        self._raise(self._cpu_scheduling)

    def _show_deadlock_detection(self) -> None:
        self._raise(self._deadlock_detection)

    def _handle_login(self, username: str, password: str) -> None:
        try:
            challenge = self._auth.begin_login(username, password)
        except AuthError as e:
            self._login.set_error(str(e))
            return
        self._login.clear_fields()
        self._show_otp(challenge.username, challenge.code)

    def _handle_register(self, username: str, password: str) -> None:
        try:
            self._auth.register(username, password)
        except AuthError as e:
            self._register.set_error(str(e))
            return
        self._register.clear_fields()
        messagebox.showinfo("Registered", "Account created. You can sign in now.")
        self._show_login()

    def _handle_otp(self, code: str) -> None:
        try:
            self._auth.complete_login(code)
        except AuthError as e:
            self._otp.set_error(str(e))
            return
        self._otp.clear_simulated()
        self._show_dashboard()

    def _cancel_otp(self) -> None:
        self._auth.cancel_otp()
        self._otp.clear_simulated()
        self._show_login()

    def _handle_logout(self) -> None:
        self._auth.logout()
        self._show_login()

    def _on_close(self) -> None:
        log_event("app_shutdown", detail="window_closed")
        self._auth.logout()
        self._auth.close()
        self.root.destroy()

