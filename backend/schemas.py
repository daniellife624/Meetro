# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None


class UserCreate(BaseModel):
    # 必填欄位
    email: EmailStr
    password: str
    username: str
    gender: str
    birthday: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    gender: Optional[str] = None
    birthday: Optional[str] = None

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
