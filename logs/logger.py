"""Central logging: file + console with timestamps."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

# Store log files under data/ so the logs package directory stays code-only
_LOG_DIR = Path(__file__).resolve().parent.parent / "data" / "logs"
_LOG_FILE = _LOG_DIR / "auth_events.log"

_configured = False


def _ensure_log_dir() -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "auth_framework") -> logging.Logger:
    global _configured
    logger = logging.getLogger(name)
    if _configured or logger.handlers:
        _configured = True
        return logger
    _ensure_log_dir()
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    _configured = True
    return logger


def log_event(
    event: str,
    *,
    username: Optional[str] = None,
    detail: Optional[str] = None,
    extra: Optional[Mapping[str, Any]] = None,
) -> None:
    """Log a domain event with optional context (no secrets)."""
    log = get_logger()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parts = [f"event={event}", f"utc={ts}"]
    if username:
        parts.append(f"user={username}")
    if detail:
        parts.append(f"detail={detail}")
    if extra:
        for k, v in extra.items():
            parts.append(f"{k}={v}")
    log.info(" | ".join(parts))
