# 包含接受邀約、邀約歷史紀錄
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel

from database import SessionLocal
from models import Match, Invite, User, Station
from auth import get_current_user

router = APIRouter(prefix="/api/matches", tags=["matches"])

# --- Pydantic Schemas ---


class MatchItemResponse(BaseModel):
    id: int
    senderName: str
    senderGender: Optional[str] = None
    stationName: str
    location: str
    status: str
    # date: str # 如果需要日期可以加


class UpdateStatusRequest(BaseModel):
    status: str


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---


@router.get("/history", response_model=List[MatchItemResponse])
def get_my_history(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # 查詢資料庫：找出所有「我是接受者」的配對
    # 使用 joinedload 預先載入關聯資料，避免 N+1 問題
    matches = (
        db.query(Match)
        .options(
            joinedload(Match.invite).joinedload(Invite.sender),
            joinedload(Match.invite).joinedload(Invite.station),
        )
        .filter(Match.receiver_id == current_user.id)
        .all()
    )

    results = []
    for m in matches:
        # 如果不想顯示已拒絕的，可以在這裡過濾
        # if m.status == 'rejected': continue

        # 將 DB 物件轉為前端需要的格式
        results.append(
            {
                "id": m.id,
                "senderName": m.invite.sender.name,
                "senderGender": m.invite.sender.gender,
                "stationName": m.invite.station.name_zh,
                "location": m.invite.location_name,
                "status": m.status,
            }
        )

    return results


@router.patch("/{match_id}/status")
def update_match_status(
    match_id: int,
    request: UpdateStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. 查詢該配對，並確認權限
    match_obj = (
        db.query(Match)
        .filter(Match.id == match_id, Match.receiver_id == current_user.id)
        .first()
    )

    if not match_obj:
        raise HTTPException(status_code=404, detail="找不到此邀約")

    # 2. 更新狀態
    match_obj.status = request.status
    db.commit()
    db.refresh(match_obj)

    return {"message": "更新成功", "status": match_obj.status}


@router.post("/{invite_id}/accept")
def accept_invite(
    invite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. 檢查邀約是否存在且開放
    invite = (
        db.query(Invite).filter(Invite.id == invite_id, Invite.status == "open").first()
    )
    if not invite:
        raise HTTPException(status_code=404, detail="邀約不存在或已關閉")

    # 2. 檢查是否自己發的 (不能接受自己的邀約)
    if invite.sender_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能接受自己的邀約")

    # 3. 檢查是否已經接受過
    existing = (
        db.query(Match)
        .filter(Match.invite_id == invite_id, Match.receiver_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="已經接受過此邀約")

    # 4. 建立 Match
    new_match = Match(
        invite_id=invite_id,
        receiver_id=current_user.id,
        status="pending",
        created_at=datetime.now(),
    )
    db.add(new_match)

    # 5. (選擇性) 將邀約狀態改為 'matched' 或保持 open 讓多人接受?
    # 這裡假設一對一，接受後就關閉
    # invite.status = "matched"

    db.commit()
    return {"message": "成功接受邀約", "match_id": new_match.id}
