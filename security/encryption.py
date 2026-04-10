"""
Optional symmetric encryption (Fernet) for sensitive in-memory / demo payloads.
Generates a runtime key so ciphertext is not persisted across app restarts.
"""

from __future__ import annotations

from cryptography.fernet import Fernet


class EncryptionService:
    def __init__(self) -> None:
        self._fernet = Fernet(Fernet.generate_key())

    def encrypt(self, plaintext: str) -> bytes:
        return self._fernet.encrypt(plaintext.encode("utf-8"))

    def decrypt(self, token: bytes) -> str:
        return self._fernet.decrypt(token).decode("utf-8")
