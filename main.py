"""
Secure Authentication Framework — application entry point.
Run from project root: python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is importable when executed as a script
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ui.app import AuthApplication


def main() -> None:
    app = AuthApplication()
    app.run()


if __name__ == "__main__":
    main()
