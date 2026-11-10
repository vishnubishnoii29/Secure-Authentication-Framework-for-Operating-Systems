"""In-memory lockout after repeated failed sign-ins for the same username."""

from __future__ import annotations

import time
from typing import Callable


class LoginThrottle:
    """Locks a username for `lock_seconds` after `max_failures` failures in a row.

    Unknown usernames are counted too, so the lockout does not reveal which
    accounts exist. State is kept in memory only: restarting the app resets it.
    """

    def __init__(
        self,
        max_failures: int = 5,
        lock_seconds: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._max = max_failures
        self._lock = lock_seconds
        self._clock = clock
        self._failures: dict[str, int] = {}
        self._locked_until: dict[str, float] = {}

    @staticmethod
    def _key(username: str) -> str:
        return username.strip().lower()

    def seconds_locked(self, username: str) -> int:
        """Whole seconds left on the lock, or 0 when the username may try."""
        key = self._key(username)
        until = self._locked_until.get(key)
        if until is None:
            return 0
        left = until - self._clock()
        if left <= 0:
            del self._locked_until[key]
            self._failures.pop(key, None)
            return 0
        return int(left) + 1

    def record_failure(self, username: str) -> None:
        key = self._key(username)
        count = self._failures.get(key, 0) + 1
        self._failures[key] = count
        if count >= self._max:
            self._locked_until[key] = self._clock() + self._lock

    def record_success(self, username: str) -> None:
        key = self._key(username)
        self._failures.pop(key, None)
        self._locked_until.pop(key, None)
