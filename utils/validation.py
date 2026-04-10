"""Input validation for registration and login."""

from __future__ import annotations

import re
from typing import Tuple


class ValidationError(Exception):
    pass


_MIN_USER_LEN = 3
_MAX_USER_LEN = 32
_MIN_PASS_LEN = 8
_MAX_PASS_LEN = 128

_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+$")


def validate_username(username: str) -> str:
    u = (username or "").strip()
    if not u:
        raise ValidationError("Username cannot be empty.")
    if len(u) < _MIN_USER_LEN:
        raise ValidationError(f"Username must be at least {_MIN_USER_LEN} characters.")
    if len(u) > _MAX_USER_LEN:
        raise ValidationError(f"Username must be at most {_MAX_USER_LEN} characters.")
    if not _USERNAME_PATTERN.match(u):
        raise ValidationError(
            "Username may only contain letters, digits, dot, underscore, and hyphen."
        )
    return u


def validate_password_strength(password: str) -> str:
    p = password or ""
    if not p:
        raise ValidationError("Password cannot be empty.")
    if len(p) < _MIN_PASS_LEN:
        raise ValidationError(f"Password must be at least {_MIN_PASS_LEN} characters.")
    if len(p) > _MAX_PASS_LEN:
        raise ValidationError(f"Password must be at most {_MAX_PASS_LEN} characters.")
    if not re.search(r"[a-z]", p):
        raise ValidationError("Password must include a lowercase letter.")
    if not re.search(r"[A-Z]", p):
        raise ValidationError("Password must include an uppercase letter.")
    if not re.search(r"\d", p):
        raise ValidationError("Password must include a digit.")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", p):
        raise ValidationError("Password must include at least one special character.")
    return p


def validate_credentials(username: str, password: str) -> Tuple[str, str]:
    return validate_username(username), validate_password_strength(password)
