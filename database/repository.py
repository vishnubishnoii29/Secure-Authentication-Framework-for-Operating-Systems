"""User data access."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from database.connection import get_connection


@dataclass
class UserRecord:
    id: int
    username: str
    password_hash: bytes
    created_at: str


class UserRepository:
    def __init__(self, connection: Optional[sqlite3.Connection] = None) -> None:
        self._external = connection is not None
        self._conn = connection or get_connection()

    def close(self) -> None:
        if not self._external:
            self._conn.close()

    def create_user(self, username: str, password_hash: bytes) -> int:
        try:
            cur = self._conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username.strip(), password_hash),
            )
            self._conn.commit()
            return int(cur.lastrowid)
        except sqlite3.IntegrityError as e:
            self._conn.rollback()
            raise DuplicateUsernameError(username) from e

    def get_by_username(self, username: str) -> Optional[UserRecord]:
        cur = self._conn.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return UserRecord(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )

    def username_exists(self, username: str) -> bool:
        cur = self._conn.execute(
            "SELECT 1 FROM users WHERE username = ? COLLATE NOCASE LIMIT 1",
            (username.strip(),),
        )
        return cur.fetchone() is not None


class DuplicateUsernameError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"Username already taken: {username}")
        self.username = username
