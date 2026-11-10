"""Tests run against a temporary log file and in-memory database, never the real data/ folder."""

import tempfile
from pathlib import Path

import logs.logger as _logger

_tmp = Path(tempfile.mkdtemp(prefix="authlog_"))
_logger._LOG_DIR = _tmp
_logger._LOG_FILE = _tmp / "auth_events.log"
