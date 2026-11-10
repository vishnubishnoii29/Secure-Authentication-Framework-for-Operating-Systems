# Secure Authentication Framework with OS Simulators

A Python and Tkinter desktop application that combines a layered authentication stack with two Operating System simulators. It works as a security mini-project and as an OS lab demonstration.

## Features

- Registration with input validation
- Password hashing with `bcrypt`
- Login with a simulated OTP (the code is shown on screen for demos)
- Lockout after repeated failures: 5 wrong passwords lock the username for 60 seconds, and an OTP is dropped after 3 wrong codes or 120 seconds
- Session token kept encrypted in memory with `cryptography` (a teaching example)
- SQLite account storage and an audit log with timestamps
- CPU scheduling simulator: FCFS, SJF, Round Robin, Priority, with Gantt output and average waiting and turnaround times
- Deadlock simulator: Banker's safe-state check and a wait-for graph, with input checks (allocation cannot exceed maximum demand, no negative values)

## Project structure

```text
main.py                 entry point
auth/                   registration, login, OTP hand-off, session, lockout (throttle.py)
security/               bcrypt hashing, OTP, Fernet encryption
database/               SQLite connection, schema, user repository
logs/                   file and console logging
os_algorithms/          cpu_scheduling.py, deadlock_detection.py
ui/                     Tkinter screens
utils/                  username and password rules
tests/                  unit tests (standard library only)
client/                 unfinished React login mock-up, not connected to the app
data/                   created at run time: auth.db and logs/auth_events.log (not in git)
FEATURES.md             notes on the OS tools
```

## Setup and run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Python 3.10 or newer. No database server is needed: `data/` is created on first run.

## Tests

```powershell
python -m unittest discover -s tests -t .
```

The tests use an in-memory database and a temporary log file, so they never touch `data/`.

## Using it

1. Register with a username (3 to 32 characters: letters, digits, `.`, `_`, `-`) and a password of 8 to 72 bytes with a lowercase letter, an uppercase letter, a digit and a special character. The 72-byte limit comes from bcrypt.
2. Sign in, then type the code shown on the OTP screen.
3. From the dashboard open the CPU Scheduling or Deadlock Detection simulator.

## Security notes

- Passwords are stored only as bcrypt hashes. Failed-login messages are the same for unknown users and wrong passwords, and unknown usernames are counted toward the lockout too.
- Lockout state is in memory, so restarting the app clears it.
- The OTP is shown on screen on purpose; a real system would send it to a phone or email.
- The encrypted session token uses a key that lives only in memory. It demonstrates encryption but does not add real session security.
- `data/` holds account hashes and the audit log and is ignored by git. Do not commit it.

## The deadlock simulator in short

- **Banker's algorithm** reports a safe state with a safe sequence, or an unsafe state with the processes that cannot be guaranteed to finish. An unsafe state is a risk of deadlock, not yet a deadlock.
- **Wait-for graph** adds an edge from a process to every holder of a resource it still needs and cannot get now. A cycle is a deadlock when each resource has one instance; with several instances, confirm it with Banker's algorithm.

## License

Educational use. Adapt as needed for coursework.
