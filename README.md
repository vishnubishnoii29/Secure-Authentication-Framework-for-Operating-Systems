
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