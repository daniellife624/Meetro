# backend/security.py
# SHA256 雜湊
import hashlib


def hash_password(password: str) -> str:
    """
    回傳密碼的 SHA256 雜湊（十六進位字串）。
    """
    # 將密碼編碼為 utf-8 才能進行雜湊
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    檢查使用者輸入的密碼，雜湊後是否和資料庫中的雜湊值相同。
    """
    # 再次雜湊明文密碼，與資料庫中的雜湊值進行比較
    return hash_password(plain_password) == hashed_password
