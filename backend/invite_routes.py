# backend/invite_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
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


# 建立邀約 (Sender)
@router.post("", response_model=backend.schemas.InviteOut)
def create_invite(
    invite_in: backend.schemas.InviteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(f"DEBUG: Received station_key from Frontend: {invite_in.station_key}")

    # 找站點
    station_key_lower = invite_in.station_key.lower()

    station = db.query(Station).filter(Station.key == station_key_lower).first()

    # 輸出站點查詢結果
    if not station:
        # 如果站點不存在，確認資料庫中到底有沒有該鍵值
        print(f"DEBUG: Station key '{station_key_lower}' NOT FOUND in DB.")
        if db.query(Station).count() == 0:
            print("DEBUG: WARNING! Station table is currently EMPTY.")

        raise HTTPException(status_code=404, detail="站點不存在")

    # 站點存在，繼續處理
    print(f"DEBUG: Station found with ID: {station.id}")

    # 處理 meet_time 轉換
    try:
        meet_time_dt = invite_in.meet_time
    except Exception:
        raise HTTPException(status_code=400, detail="Meet time 格式無效")

    new_invite = Invite(
        sender_id=current_user.id,
        station_id=station.id,
        title=invite_in.title,
        meet_time=meet_time_dt,
        location_name=invite_in.location_name,
        latitude=invite_in.latitude,
        longitude=invite_in.longitude,
        status="open",
    )

    try:
        db.add(new_invite)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DEBUG: DB Commit Error: {e.__class__.__name__} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"資料庫寫入錯誤: {e.__class__.__name__}. 請檢查 Invite Model 的非空約束。",
        )

    db.refresh(new_invite)
    return new_invite


# 查詢某站點的邀約 (Receiver)
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
