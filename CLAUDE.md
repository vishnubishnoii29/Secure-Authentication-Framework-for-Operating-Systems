# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Windows/PowerShell, Python 3.10+. Dependencies are only `bcrypt` and `cryptography`; the GUI uses stdlib Tkinter.

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py                                   # run the desktop app
python -m unittest discover -s tests -t .        # all tests (-t . is required so package imports resolve)
python -m unittest tests.test_auth.SomeClass.test_name   # single test
```

There is no linter or build step.

## Architecture

A Tkinter app with two layers that never import each other: an authentication stack and two OS-algorithm simulators. `ui/` is the only place that wires them together.

- **`ui/app.py` (`AuthApplication`)** builds every screen once (login, register, OTP, dashboard, CPU scheduling, deadlock) as stacked frames placed over each other and switches with `tkraise()`. It owns a single `AuthService` and routes `AuthError` messages to the views. Screens do not call `AuthService` directly; they take callbacks.
- **`auth/service.py` (`AuthService`)** is the login state machine: `begin_login` (validate, check throttle, bcrypt verify, issue OTP) then `complete_login` (verify OTP, create `SessionState`). Collaborators (`UserRepository`, `LoginThrottle`, `OTPService`) are injectable via the constructor, which is how tests avoid real state. Failed logins return the same message for unknown users and bad passwords, and unknown usernames are counted toward lockout. A dead OTP challenge (3 wrong codes or 120 s) counts as a throttle failure.
- **`auth/throttle.py`** is in-memory only; the clock is injectable (`clock=`) for tests.
- **`security/`**: bcrypt hashing (passwords are capped at 72 bytes, enforced in `utils/validation.py`), OTP issue/verify, Fernet `EncryptionService` whose key lives only in memory (demo of encrypting the session token).
- **`database/`**: SQLite via `connection.py` (path `data/auth.db`, schema in `init_database`) and `repository.py`. Passing an in-memory connection is how tests avoid touching `data/`.
- **`audit/logger.py`**: `log_event(event, username=..., detail=...)` writes the audit log to `data/logs/auth_events.log`. Use it for any new auth event.
- **`os_algorithms/`**: pure logic, no UI imports. `cpu_scheduling.py` (`CPUScheduler`: FCFS, SJF, Round Robin, Priority, Gantt + avg waiting/turnaround; only Round Robin is preemptive, SJF and Priority are non-preemptive, lower priority number wins) and `deadlock_detection.py` (`DeadlockDetector`: Banker's safe-state check and wait-for graph; `validate_state` rejects allocation > max and negative values). The `ui/*_view.py` files only collect input and render results.

`data/` is created at run time and git-ignored (it holds account hashes and the audit log); never commit it. `README.md` documents the user-facing behaviour and the OS tools; keep it in sync when changing algorithms or lockout limits (5 failures / 60 s lock, OTP 6 digits / 120 s / 3 attempts).
