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


# 繪馬
class EmaCreate(BaseModel):
    station_key: str  # 前端傳來站點代號 (e.g. 'songshan')
    location: str  # 探索地點名稱
    content: str  # 心得
    photo_url: Optional[str] = None  # 照片 (Base64 或 URL)


class EmaOut(BaseModel):
    id: int
    userName: str  # 為了配合前端 EmaCard，直接回傳姓名
    location: str  # 對應 location_text
    content: str
    photoUrl: Optional[str] = None
    date: str  # 格式化後的日期字串

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

    # 🚨 關鍵新增：發送方的基本資訊
    sender: SenderInfo
    # 🚨 關鍵新增：發送方的模擬成功率
    sender_success_rate: float

    class Config:
        from_attributes = True
