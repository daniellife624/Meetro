# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBasic(BaseModel):
    email: EmailStr
    name: str | None = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
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


# 繪馬
class EmaCreate(BaseModel):
    station_key: str
    location: str
    content: str
    photo_url: Optional[str] = None  # 照片 (Base64 或 URL)


class EmaOut(BaseModel):
    id: int
    userName: str
    location: str
    content: str
    photoUrl: Optional[str] = None
    date: str

    class Config:
        from_attributes = True


# 邀約
class InviteCreate(BaseModel):
    title: str
    meet_time: datetime
    location_name: str
    latitude: float
    longitude: float
    station_key: str


class InviteOut(BaseModel):
    id: int
    title: str
    meet_time: datetime
    location_name: str
    latitude: float
    longitude: float
    sender: UserBasic

    class Config:
        from_attributes = True


# 發送方的基本資訊 (與 UserBasic 相同，但確保結構清晰)
class SenderInfo(BaseModel):
    id: int
    name: str | None = None

    class Config:
        from_attributes = True


# 邀約列表的單項輸出 (包含發送方成功率)
class InviteOutWithSuccessRate(BaseModel):
    id: int
    title: str
    meet_time: datetime
    location_name: str
    latitude: float
    longitude: float
    sender: SenderInfo
    sender_success_rate: float

    class Config:
        from_attributes = True
