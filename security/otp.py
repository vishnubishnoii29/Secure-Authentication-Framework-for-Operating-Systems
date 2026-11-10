"""Time-limited random OTP for simulated MFA."""

from __future__ import annotations

import secrets
import string
import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(slots=True)
class OTPChallenge:
    code: str
    expires_at: float
    username: str
    attempts_left: int


class OTPService:
    """Generates numeric OTPs and holds a single pending challenge per flow.

    A challenge is dropped after `max_attempts` wrong guesses, so the code
    cannot be found by trying every number.
    """

    def __init__(
        self,
        length: int = 6,
        ttl_seconds: float = 120.0,
        max_attempts: int = 3,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._length = length
        self._ttl = ttl_seconds
        self._max_attempts = max_attempts
        self._clock = clock
        self._pending: Optional[OTPChallenge] = None

    def issue(self, username: str) -> OTPChallenge:
        digits = string.digits
        code = "".join(secrets.choice(digits) for _ in range(self._length))
        challenge = OTPChallenge(
            code=code,
            expires_at=self._clock() + self._ttl,
            username=username,
            attempts_left=self._max_attempts,
        )
        self._pending = challenge
        return challenge

    def verify(self, username: str, entered: str) -> bool:
        if self._pending is None:
            return False
        p = self._pending
        if p.username != username.strip():
            return False
        if self._clock() > p.expires_at:
            self._pending = None
            return False
        ok = secrets.compare_digest(p.code.strip(), entered.strip())
        if ok:
            self._pending = None
            return True
        p.attempts_left -= 1
        if p.attempts_left <= 0:
            self._pending = None
        return False

    @property
    def has_pending(self) -> bool:
        return self._pending is not None

    def clear(self) -> None:
        self._pending = None
