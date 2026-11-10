# Features and OS Tools

Notes on what the application does, with a closer look at the two Operating System simulators. For setup, tests and security notes see `README.md`.

## Authentication

- Registration with username and password rules (`utils/validation.py`)
- Password hashing with `bcrypt` (72-byte limit)
- Login with a simulated OTP; the code is shown on screen for demonstration
- Lockout: 5 wrong passwords lock the username for 60 seconds; an OTP is dropped after 3 wrong codes or 120 seconds (`auth/throttle.py`). State is in memory, so a restart clears it
- Session token encrypted in memory with `cryptography` (a teaching example)
- SQLite account storage and an audit log with timestamps

## CPU Scheduling Simulator

- **Location**: Dashboard, "Open CPU Scheduler"
- **Algorithms**:
  - **FCFS** (First Come First Served), non-preemptive
  - **SJF** (Shortest Job First), non-preemptive
  - **Priority** (a lower number means a higher priority), non-preemptive
  - **Round Robin** with a configurable time quantum, preemptive
- **Features**:
  - Add, remove and clear processes with arrival time, burst time and priority
  - Gantt chart of the execution timeline
  - Waiting time and turnaround time per process, with averages for comparison

## Deadlock Simulator

- **Location**: Dashboard, "Open Deadlock Detector"
- **Methods**:
  - **Banker's algorithm**: reports a safe state with a safe sequence, or an unsafe state with the processes that cannot be guaranteed to finish. An unsafe state is a risk of deadlock, not yet a deadlock
  - **Wait-for graph**: an edge from a process to every holder of a resource it still needs and cannot get now. A cycle is a deadlock when each resource has one instance; with several instances, confirm it with Banker's algorithm
- **Features**:
  - Set the number of processes and resources
  - Enter allocation, maximum demand and available resources
  - Input checks: no negative values, and allocation cannot exceed maximum demand
  - Need matrix (maximum minus allocation), safe sequence and the list of deadlocked processes

## Project structure

```text
main.py                       entry point
auth/                         registration, login, OTP hand-off, session, lockout
security/                     bcrypt hashing, OTP, Fernet encryption
database/                     SQLite connection, schema, user repository
logs/                         file and console logging
utils/                        username and password rules
os_algorithms/
  cpu_scheduling.py           FCFS, SJF, Round Robin, Priority
  deadlock_detection.py       Banker's algorithm, wait-for graph
ui/
  app.py                      main window and screen routing
  login_view.py, register_view.py, otp_view.py
  dashboard_view.py           feature cards for the two simulators
  cpu_scheduling_view.py      CPU Scheduling Simulator screen
  deadlock_detection_view.py  Deadlock Simulator screen
  styles.py                   dark theme and widget styles
tests/                        unit tests (standard library only)
client/                       unfinished React mock-up, not connected to the app
```

## Using the simulators

### CPU Scheduling

1. Sign in, then open "Open CPU Scheduler" on the dashboard
2. Add processes with arrival time, burst time and priority
3. Choose an algorithm; for Round Robin also set the time quantum
4. Click "Calculate & View Results" to see the Gantt chart, waiting times and turnaround times

### Deadlock Detection

1. Sign in, then open "Open Deadlock Detector" on the dashboard
2. Set the number of processes and resources
3. Enter the allocation matrix, the maximum demand matrix and the available resources
4. Choose Banker's algorithm or the wait-for graph and click "Analyze for Deadlock"
5. Read the result, the need matrix and the safe sequence

## Tests

The scheduling, deadlock and authentication logic is covered by unit tests (`python -m unittest discover -s tests -t .`). The Tkinter screens are not covered by automated tests.
