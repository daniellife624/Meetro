# backend/history_routes.py (完整程式碼)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


from backend.database import SessionLocal
from backend.models import Match, Invite, User, Station
from backend.auth import get_current_user
import datetime


router = APIRouter(prefix="/api/matches", tags=["matches"])

# --- Pydantic Schemas ---


# 🚨 新增/修正：歷史紀錄回傳結構
class MatchItemResponse(BaseModel):
    id: int
    partnerName: str  # 👈 顯示對方的名字
    partnerGender: Optional[str] = None  # 👈 顯示對方的性別
    stationName: str
    location: str
    status: str
    inviteDate: datetime

    # 🚨 新增：評分欄位
    sender_rating: Optional[int] = None
    receiver_rating: Optional[int] = None

    # 🚨 新增：角色標誌
    is_current_user_sender: bool  # 判斷當前使用者是發送方還是接受方

    class Config:
        from_attributes = True


class UpdateStatusRequest(BaseModel):
    status: str  # 期望值: "confirmed", "rejected", ...


# 🚨 新增：評分請求 Pydantic
class FeedbackRequest(BaseModel):
    rating: int  # 接收 0-100 的數字


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
    # 🚨 修正：找出所有「我是接受者」或「我是發送者」的配對
    matches = (
        db.query(Match)
        .options(
            joinedload(Match.invite).joinedload(Invite.sender),
            joinedload(Match.invite).joinedload(Invite.station),
            joinedload(Match.receiver),  # 載入 Match 的 receiver 關聯
        )
        .join(Invite)
        .filter(
            (Match.receiver_id == current_user.id)
            | (Invite.sender_id == current_user.id)
        )
        .all()
    )

    results = []
    for m in matches:
        if (
            not m.invite
            or not m.invite.sender
            or not m.invite.station
            or not m.receiver
        ):
            continue

        is_current_user_sender = m.invite.sender_id == current_user.id

        if is_current_user_sender:
            partner = m.receiver  # 對方是 Receiver
        else:
            partner = m.invite.sender  # 對方是 Sender

        results.append(
            {
                "id": m.id,
                "partnerName": partner.name,
                "partnerGender": partner.gender if partner.gender else "未設定",
                "stationName": m.invite.station.name_zh,
                "location": m.invite.location_name,
                "status": m.status,
                "inviteDate": m.invite.meet_time,
                "sender_rating": m.sender_rating,
                "receiver_rating": m.receiver_rating,
                "is_current_user_sender": is_current_user_sender,  # 回傳角色標誌
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
    # 1. 查詢該配對，並確認權限 (只能修改自己作為 Receiver 的 Match 狀態)
    match_obj = (
        db.query(Match)
        .filter(Match.id == match_id, Match.receiver_id == current_user.id)
        .first()
    )

    if not match_obj:
        raise HTTPException(status_code=404, detail="找不到此邀約")

    # 🚨 檢查狀態有效性
    if request.status not in ["confirmed", "rejected"]:
        raise HTTPException(status_code=400, detail="無效的狀態值")

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
    # ... (保持原有的 accept_invite 邏輯，確保寫入 status="pending")
    # ... (這裡不需要動)

    # 為了完整性，這裡提供完整的 accept_invite 邏輯
    invite = (
        db.query(Invite).filter(Invite.id == invite_id, Invite.status == "open").first()
    )
    if not invite:
        raise HTTPException(status_code=404, detail="邀約不存在或已關閉")

    if invite.sender_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能接受自己的邀約")

    existing = (
        db.query(Match)
        .filter(Match.invite_id == invite_id, Match.receiver_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="已經接受過此邀約")

    new_match = Match(
        invite_id=invite_id,
        receiver_id=current_user.id,
        status="pending",
        created_at=datetime.now(),
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return {
        "message": "成功送出配對請求",
        "match_id": new_match.id,
        "invite_status": invite.status,
    }


# 🚨 新增：滿意度回饋 API
@router.post("/{match_id}/feedback")
def submit_feedback(
    match_id: int,
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. 檢查評分數值是否合法
    if not 0 <= request.rating <= 100:
        raise HTTPException(status_code=400, detail="滿意度評分必須介於 0 到 100 之間")

    # 2. 查詢 Match 紀錄
    match_obj = (
        db.query(Match)
        .options(
            joinedload(Match.invite).joinedload(Invite.sender),  # 載入 Sender
            joinedload(Match.receiver),  # 載入 Receiver
        )
        .filter(Match.id == match_id)
        .first()
    )
    if match_obj.status != "confirmed":
        raise HTTPException(status_code=400, detail="只能對已確認赴約的紀錄進行評分")

    # 3. 判斷提交者身份
    is_sender = match_obj.invite.sender_id == current_user.id
    is_receiver = match_obj.receiver_id == current_user.id

    if not is_sender and not is_receiver:
        raise HTTPException(status_code=403, detail="您不是此配對的參與者")

    # 4. 寫入評分
    if is_sender:
        if match_obj.sender_rating is not None:
            raise HTTPException(status_code=400, detail="發送方已提交過評分")
        match_obj.sender_rating = request.rating

        # 更新 feedback_status
        if match_obj.receiver_rating is not None:
            match_obj.feedback_status = "both_done"
        else:
            match_obj.feedback_status = "sender_done"

    elif is_receiver:
        if match_obj.receiver_rating is not None:
            raise HTTPException(status_code=400, detail="接受方已提交過評分")
        match_obj.receiver_rating = request.rating

        # 更新 feedback_status
        if match_obj.sender_rating is not None:
            match_obj.feedback_status = "both_done"
        else:
            match_obj.feedback_status = "receiver_done"

    # 🚨 處理：如果 status 不是 confirmed，提醒使用者
    if match_obj.status != "confirmed":
        print(
            f"DEBUG: Feedback submitted for Match {match_id} which is still {match_obj.status}"
        )

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # 🚨 捕獲 DB 錯誤，確保不返回前端「未知錯誤」
        print(f"DB COMMIT ERROR: {e}")
        raise HTTPException(status_code=500, detail="資料庫寫入滿意度失敗")

    return {"message": "滿意度提交成功", "feedback_status": match_obj.feedback_status}
