# backend/security.py
# 簡化版密碼雜湊：用標準庫 hashlib.sha256，不再用 passlib / bcrypt

import hashlib


def hash_password(password: str) -> str:
    """
    回傳密碼的 SHA256 雜湊（十六進位字串）
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    檢查使用者輸入的密碼，雜湊後是否和資料庫中的雜湊值相同
    """
    return hash_password(plain_password) == hashed_password
