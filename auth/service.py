"""Registration, login (with OTP), and session management."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Optional

from database.repository import DuplicateUsernameError, UserRepository
from logs.logger import log_event
from security.encryption import EncryptionService
from security.hashing import hash_password, verify_password
from security.otp import OTPChallenge, OTPService
from utils.validation import ValidationError, validate_credentials, validate_username


class AuthError(Exception):
    """User-facing authentication failures."""


@dataclass(slots=True)
class SessionState:
    user_id: int
    username: str
    created_at: str
    # Demo: session integrity token stored encrypted in memory
    _session_secret_cipher: bytes
    _encryption: EncryptionService

    @property
    def session_display_token(self) -> str:
        """Decrypt for dashboard display (demo of optional encryption)."""
        return self._encryption.decrypt(self._session_secret_cipher)


class AuthService:
    def __init__(self) -> None:
        self._repo = UserRepository()
        self._otp = OTPService(length=6, ttl_seconds=120.0)
        self._encryption = EncryptionService()
        self._session: Optional[SessionState] = None
        self._otp_username: Optional[str] = None

    def close(self) -> None:
        self._repo.close()

    @property
    def session(self) -> Optional[SessionState]:
        return self._session

    @property
    def pending_otp_username(self) -> Optional[str]:
        return self._otp_username

    def register(self, username: str, password: str) -> None:
        try:
            user, pwd = validate_credentials(username, password)
        except ValidationError as e:
            log_event("registration_failed", username=username.strip() or None, detail=str(e))
            raise AuthError(str(e)) from e
        try:
            ph = hash_password(pwd)
            self._repo.create_user(user, ph)
        except DuplicateUsernameError:
            log_event("registration_failed", username=user, detail="duplicate_username")
            raise AuthError("That username is already registered.") from None
        log_event("registration_success", username=user)

    def begin_login(self, username: str, password: str) -> OTPChallenge:
        """Validate credentials and start OTP step."""
        try:
            user = validate_username(username)
        except ValidationError as e:
            log_event("login_failed", username=username.strip() or None, detail=str(e))
            raise AuthError(str(e)) from e
        if not (password or "").strip():
            log_event("login_failed", username=user, detail="empty_password")
            raise AuthError("Password cannot be empty.")

        record = self._repo.get_by_username(user)
        if record is None or not verify_password(password, record.password_hash):
            # Same message to avoid user enumeration
            log_event("login_failed", username=user, detail="invalid_credentials")
            raise AuthError("Invalid username or password.")

        challenge = self._otp.issue(record.username)
        self._otp_username = record.username
        log_event("otp_issued", username=record.username, detail="mfa_challenge_created")
        return challenge

    def complete_login(self, otp_code: str) -> SessionState:
        if not self._otp_username:
            log_event("otp_failed", detail="no_pending_challenge")
            raise AuthError("No login in progress. Start again from the login screen.")
        if not (otp_code or "").strip():
            raise AuthError("OTP cannot be empty.")

        ok = self._otp.verify(self._otp_username, otp_code)
        if not ok:
            log_event("otp_failed", username=self._otp_username, detail="invalid_or_expired")
            raise AuthError("Invalid or expired OTP. Try logging in again.")

        record = self._repo.get_by_username(self._otp_username)
        self._otp_username = None
        if record is None:
            raise AuthError("Account not found.")

        secret_plain = secrets.token_urlsafe(24)
        cipher = self._encryption.encrypt(secret_plain)
        self._session = SessionState(
            user_id=record.id,
            username=record.username,
            created_at=record.created_at,
            _session_secret_cipher=cipher,
            _encryption=self._encryption,
        )
        log_event("login_success", username=record.username, detail="otp_verified")
        return self._session

    def cancel_otp(self) -> None:
        if self._otp_username:
            log_event("otp_cancelled", username=self._otp_username)
        self._otp.clear()
        self._otp_username = None

    def logout(self) -> None:
        if self._session:
            log_event("logout", username=self._session.username)
        self._session = None
        self._otp.clear()
        self._otp_username = None
