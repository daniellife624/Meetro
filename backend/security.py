# backend/security.py
# SHA256 雜湊
import hashlib


def hash_password(password: str) -> str:
    """
    回傳密碼的 SHA256 雜湊（十六進位字串）。
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    檢查使用者輸入的密碼，雜湊後是否和資料庫中的雜湊值相同。
    """
    return hash_password(plain_password) == hashed_password
