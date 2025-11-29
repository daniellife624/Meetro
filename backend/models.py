# backend/models.py
# 資料表定義
# 之後如果想手動塞一個 admin，可以直接進 DB 把某個 user 的 role 改成 "admin"
from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
