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
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# 1. 會員表 (Users)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    birthday = Column(String, nullable=True)

    role = Column(String, default="user")
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 關聯
    invites_sent = relationship("Invite", back_populates="sender")
    matches_received = relationship("Match", back_populates="receiver")
    emas = relationship("Ema", back_populates="user")


# 2. 捷運站表
class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    name_zh = Column(String, nullable=False)
    line_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

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
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    meet_time = Column(DateTime, nullable=False)
    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", back_populates="invites_sent")
    station = relationship("Station", back_populates="invites")
    matches = relationship("Match", back_populates="invite")


# 5. 配對表
class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    invite_id = Column(Integer, ForeignKey("invites.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    satisfaction_score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invite = relationship("Invite", back_populates="matches")
    receiver = relationship("User", back_populates="matches_received")


# 6. 繪馬表
class Ema(Base):
    __tablename__ = "emas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    content = Column(Text, nullable=False)
    location_text = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="emas")
    station = relationship("Station", back_populates="emas")


# 7. 後台參數表
class SystemVariable(Base):
    __tablename__ = "system_variables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    weight = Column(Integer, default=0)
    rule_desc = Column(Text, nullable=True)
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
