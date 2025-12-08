# backend/invite_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from backend.database import SessionLocal
from backend.models import Invite, Station, User, Match
from backend.auth import get_current_user
import backend.schemas

router = APIRouter(prefix="/api/invites", tags=["invites"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. 建立邀約 (Sender)
# 這個我們之前在 SenderView 做過了，但可能只是 print log，現在補上後端
@router.post("", response_model=backend.schemas.InviteOut)  # 修改：使用 schemas.InviteOut
def create_invite(
    invite_in: backend.schemas.InviteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 找站點
    station = (
        db.query(Station).filter(Station.key == invite_in.station_key.lower()).first()
    )
    if not station:
        raise HTTPException(status_code=404, detail="站點不存在")

    new_invite = Invite(
        sender_id=current_user.id,
        station_id=station.id,
        title=invite_in.title,
        meet_time=invite_in.meet_time,
        location_name=invite_in.location_name,
        latitude=invite_in.latitude,
        longitude=invite_in.longitude,
        status="open",
        created_at=datetime.now(),
    )
    db.add(new_invite)
    db.commit()
    db.refresh(new_invite)
    return new_invite


# 2. 查詢某站點的邀約 (Receiver)
@router.get("", response_model=List[backend.schemas.InviteOut])
def get_invites(station_key: str = Query(...), db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.key == station_key.lower()).first()
    if not station:
        return []

    # 查詢該站點所有 status='open' 的邀約
    # 預載 sender 資訊
    invites = (
        db.query(Invite)
        .options(joinedload(Invite.sender), joinedload(Invite.station))
        .filter(Invite.station_id == station.id, Invite.status == "open")
        .order_by(Invite.meet_time.asc())
        .all()
    )

    return invites
