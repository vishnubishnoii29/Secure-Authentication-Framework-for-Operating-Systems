
# Secure Authentication Framework for Operating Systems

A desktop demo of a layered authentication stack: **bcrypt** password hashing, **SQLite** persistence, **OTP-based MFA** (simulated delivery), optional **Fernet** encryption for an in-memory session token, structured **logging**, and a **Tkinter** UI with clear navigation between login, registration, OTP, and dashboard screens.

## Architecture

| Package      | Role |
|-------------|------|
| `ui/`       | Tkinter views and main window controller |
| `auth/`     | Registration, login flow, OTP handoff, session state |
| `security/` | bcrypt hashing, OTP generation, Fernet encryption |
| `database/` | SQLite connection, schema, user repository |
| `logs/`     | File + console logging with timestamps |
| `utils/`    | Username/password validation rules |

Runtime data:

- `data/auth.db` — user accounts
- `data/logs/auth_events.log` — audit trail

## Prerequisites

- Python 3.10+ recommended
- Windows, macOS, or Linux

## Setup

1. Open a terminal in the project root (the folder that contains `main.py`).

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python main.py
```

## Demo flow

1. **Register** — Choose a username and a strong password (minimum 8 characters, upper and lower case, digit, special character).
2. **Login** — Enter credentials; the app issues a one-time code.
3. **OTP** — The code is shown as a **simulated** on-screen “delivery” for lab/demo use; enter it to complete sign-in.
4. **Dashboard** — Welcome message, account metadata, and a sample **session integrity token** decrypted from memory (demonstrates the encryption helper).
5. **Log out** — Clears session and returns to login.

## Security notes (evaluation context)

- Passwords are never stored in plain text; only **bcrypt** hashes are saved.
- Failed login messages are generic to reduce **user enumeration**.
- OTP is short-lived (default **120 seconds**) and cleared after success or cancel.
- This is a **teaching UI**: showing the OTP on screen is intentional for demos, not production practice.

## License

Educational use — adapt as needed for coursework.
=======
# Secure-Authentication-Framework-for-Operating-Systems
This project presents a robust and scalable authentication framework designed to enhance the security of operating systems by ensuring that only authorized users gain access to system resources. The framework integrates modern authentication techniques, including secure password handling, multi-factor authentication (MFA).
(no <<<<< >>>>>)
=======
# Secure Authentication Framework with OS Simulators

This project is a desktop application built with Python and Tkinter. It combines a secure authentication workflow with educational Operating System tools, making it useful both as a security mini-project and as an OS lab demonstration.

The application supports user registration, password hashing, simulated OTP-based login, SQLite-backed account storage, event logging, CPU scheduling simulation, and deadlock detection analysis through a single graphical interface.

## Features

- User registration with input validation
- Password hashing with `bcrypt`
- Two-factor login flow with a simulated OTP
- Session token generation with in-memory encryption using `cryptography`
- SQLite database for local account storage
- Audit-style authentication logs saved to disk
- CPU scheduling simulator with:
  - FCFS
  - SJF
  - Round Robin
  - Priority Scheduling
- Deadlock detection simulator with:
  - Banker's Algorithm
  - Wait-for Graph cycle detection
- Tkinter dashboard for navigating all modules

## Tech Stack

- Python 3.10+
- Tkinter for the desktop UI
- SQLite for persistence
- `bcrypt` for password hashing
- `cryptography` for symmetric encryption

Verified in this workspace with Python `3.14.4`.

## Project Structure

```text
.
|-- main.py
|-- FEATURES.md
|-- auth/
|   `-- service.py
|-- database/
|   |-- connection.py
|   `-- repository.py
|-- data/
|   |-- auth.db
|   `-- logs/
|       `-- auth_events.log
|-- logs/
|   `-- logger.py
|-- os_algorithms/
|   |-- cpu_scheduling.py
|   `-- deadlock_detection.py
|-- security/
|   |-- encryption.py
|   |-- hashing.py
|   `-- otp.py
|-- ui/
|   |-- app.py
|   |-- dashboard_view.py
|   |-- login_view.py
|   |-- register_view.py
|   |-- otp_view.py
|   |-- cpu_scheduling_view.py
|   |-- deadlock_detection_view.py
|   `-- styles.py
`-- utils/
    `-- validation.py
```

## How It Works

### Authentication Flow

1. A user registers with a validated username and strong password.
2. The password is hashed with `bcrypt` before being stored.
3. During login, the app verifies the password and issues a one-time password.
4. The OTP is displayed inside the app for demo purposes.
5. After OTP verification, the app creates a session object and stores a demo session token encrypted in memory.

### Operating System Tools

After login, the dashboard provides access to two interactive OS modules:

- CPU Scheduling Simulator
  - Add processes with arrival time, burst time, and priority
  - Compare waiting time and turnaround time across algorithms
  - View the execution timeline in a Gantt-chart-style output
- Deadlock Detection Simulator
  - Configure processes and resources
  - Enter allocation, maximum demand, and available resources
  - Analyze the system using Banker's Algorithm or a Wait-for Graph approach

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install bcrypt cryptography
```

### 3. Run the application

```powershell
python main.py
```

## Usage

### Register and Login

1. Start the app.
2. Create a new account from the registration screen.
3. Sign in with the same credentials.
4. Use the OTP shown on the verification screen to complete login.

### Explore the Dashboard

Once logged in, you can:

- view the current session details
- open the CPU Scheduling Simulator
- open the Deadlock Detection Simulator
- log out safely

## Generated Files

The application creates or uses these local files during runtime:

- `data/auth.db` for stored user accounts
- `data/logs/auth_events.log` for authentication and app event logs

No external database server is required.

## Validation and Security Notes

- Usernames must be 3 to 32 characters long and may contain letters, digits, `.`, `_`, and `-`
- Passwords must be 8 to 128 characters long and include:
  - one lowercase letter
  - one uppercase letter
  - one digit
  - one special character
- OTP verification is simulated for demonstration purposes
- Session token encryption is runtime-only and intended as a teaching example

## Educational Value

This project demonstrates how security concepts and OS concepts can be combined in one application:

- authentication and access control
- password hashing and secure verification
- OTP-based multi-step login flow
- session handling
- CPU scheduling analysis
- deadlock detection and safe-state reasoning

## Additional Notes

- `FEATURES.md` contains a more feature-focused summary of the OS tools and UI improvements.
- The project is designed as a local desktop application, so all data stays on the machine unless you extend it further.