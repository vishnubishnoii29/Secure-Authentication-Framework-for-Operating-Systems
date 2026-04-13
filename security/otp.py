"""Time-limited random OTP for simulated MFA."""

from __future__ import annotations

import secrets
import string
import time
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class OTPChallenge:
    code: str
    expires_at: float
    username: str


class OTPService:
    """Generates numeric OTPs and holds a single pending challenge per flow."""

    def __init__(self, length: int = 6, ttl_seconds: float = 120.0) -> None:
        self._length = length
        self._ttl = ttl_seconds
        self._pending: Optional[OTPChallenge] = None

    def issue(self, username: str) -> OTPChallenge:
        digits = string.digits
        code = "".join(secrets.choice(digits) for _ in range(self._length))
        challenge = OTPChallenge(
            code=code,
            expires_at=time.monotonic() + self._ttl,
            username=username,
        )
        self._pending = challenge
        return challenge

    def verify(self, username: str, entered: str) -> bool:
        if self._pending is None:
            return False
        p = self._pending
        if p.username != username.strip():
            return False
        if time.monotonic() > p.expires_at:
            self._pending = None
            return False
        ok = secrets.compare_digest(p.code.strip(), entered.strip())
        if ok:
            self._pending = None
        return ok

    def clear(self) -> None:
        self._pending = None
