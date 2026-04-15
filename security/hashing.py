"""bcrypt password hashing."""

from __future__ import annotations

import bcrypt


def hash_password(plain_password: str) -> bytes:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt(rounds=12))


def verify_password(plain_password: str, password_hash: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash)
    except (ValueError, TypeError):
        return False
