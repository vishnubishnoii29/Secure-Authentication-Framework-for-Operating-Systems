"""Database layer: SQLite connection and user persistence."""

from database.connection import get_connection, init_database
from database.repository import UserRepository

__all__ = ["get_connection", "init_database", "UserRepository"]
