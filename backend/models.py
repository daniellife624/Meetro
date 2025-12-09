# backend/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Float,
    Text,
    DateTime,
    Enum,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


# 1. 會員表 (Users)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String(20), nullable=False)
    gender = Column(String, nullable=True)
    birthday = Column(String, nullable=True)

    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 關聯
    invites_sent = relationship("Invite", back_populates="sender")
    matches_received = relationship(
        "Match",
        back_populates="receiver",
        foreign_keys="[Match.receiver_id]",  # 使用 Match 中的 receiver_id 指向 User.id
    )
    matches_sent = relationship(
        "Match",
        back_populates="sender",
        foreign_keys="[Match.sender_id]",  # 使用 Match 中的 sender_id 指向 User.id
    )
    emas = relationship("Ema", back_populates="user")


# 2. 捷運站表
class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True)
    name_zh = Column(String, nullable=False)
    line_code = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    attractions = relationship("Attraction", back_populates="station")
    invites = relationship("Invite", back_populates="station")
    emas = relationship("Ema", back_populates="station")


# 3. 景點表
class Attraction(Base):
    __tablename__ = "attractions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"))
    station = relationship("Station", back_populates="attractions")


# 4. 邀約表
class Invite(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    meet_time = Column(DateTime, nullable=False)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String(20), default="open", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", back_populates="invites_sent")
    station = relationship("Station", back_populates="invites")
    matches = relationship("Match", back_populates="invite")
    # matches_list = relationship("Match", back_populates="invite")


# 5. 配對表
class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    invite_id = Column(Integer, ForeignKey("invites.id"))
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Integer, default=1, nullable=False)  # pending, confirmed, rejected
    satisfaction_score = Column(Integer, nullable=True)
    __table_args__ = (
        CheckConstraint("satisfaction_score <= 100", name="satisfaction_score_max_100"),
    )
    # feedback = Column(Text, nullable=True)
    # 滿意度評分欄位 (0-100)
    sender_rating = Column(Integer, nullable=True)  # 發送方的評分
    receiver_rating = Column(Integer, nullable=True)  # 接受方的評分
    # 評分狀態追蹤
    feedback_status = Column(
        String(20), default="pending", nullable=False
    )  # 'pending', 'sender_done', 'receiver_done', 'both_done'
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invite = relationship("Invite", back_populates="matches")
    receiver = relationship("User", foreign_keys=[receiver_id])
    sender = relationship("User", foreign_keys=[sender_id])


# 6. 繪馬表
class Ema(Base):
    __tablename__ = "emas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    content = Column(String(50), nullable=False)
    location_text = Column(String(100), nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="emas")
    station = relationship("Station", back_populates="emas")


# 7. 後台參數表
class SystemVariable(Base):
    __tablename__ = "system_variables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    weight = Column(Integer, default=0)
    rule_desc = Column(String(100), nullable=True)
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
