import base64
import hashlib
import hmac
import os
import time
from dataclasses import dataclass


SESSION_TTL_SECONDS = 60 * 60 * 12  # 12 horas


@dataclass
class SessionData:
    user_id: int
    issued_at: int


def _get_secret() -> bytes:
    secret = os.getenv("APP_SECRET", "dev-secret-change-me")
    return secret.encode("utf-8")


def hash_password(password: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return base64.b64encode(salt + dk).decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    raw = base64.b64decode(stored_hash.encode("utf-8"))
    salt, expected = raw[:16], raw[16:]
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(dk, expected)


def create_session_cookie(user_id: int) -> str:
    issued_at = int(time.time())
    payload = f"{user_id}:{issued_at}".encode("utf-8")
    signature = hmac.new(_get_secret(), payload, hashlib.sha256).digest()
    token = base64.b64encode(payload + b"." + signature).decode("utf-8")
    return token


def parse_session_cookie(cookie_value: str) -> SessionData | None:
    try:
        decoded = base64.b64decode(cookie_value.encode("utf-8"))
        payload, signature = decoded.rsplit(b".", 1)
        expected = hmac.new(_get_secret(), payload, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            return None
        user_id_str, issued_at_str = payload.decode("utf-8").split(":")
        issued_at = int(issued_at_str)
        if int(time.time()) - issued_at > SESSION_TTL_SECONDS:
            return None
        return SessionData(user_id=int(user_id_str), issued_at=issued_at)
    except Exception:
        return None
