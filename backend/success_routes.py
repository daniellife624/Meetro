from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from backend.database import SessionLocal
from backend.auth import get_current_user
from backend.models import User, Match, Invite, SystemVariable
from backend.services.success_rate_service import get_bcms_weights
from backend.weather_routes import compute_weather_score


router = APIRouter(prefix="/api/success", tags=["success"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 確保 compute_place_score 在您的專案中已定義
def compute_place_score(lat: float, lng: float) -> float:
    """模擬計算地點景點熱門程度得分 (0-100)"""
    return 85.0


@router.get("/estimate")
def estimate_success_rate(
    station_key: str = Query(..., description="捷運站 key，例如 ximen"),
    lat: float = Query(..., description="地點緯度"),
    lng: float = Query(..., description="地點經度"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    估算使用者在下次邀約中潛在的成功率。
    只要對方已評分，即可納入歷史滿意度計算 (動態權重)。
    """
    weights = get_bcms_weights(db)

    # 確保所有權重都存在 (使用 .get() 獲取，若不存在則使用 service 層的預設值)
    W_HISTORY = weights.get("history", 0.50)
    W_WEATHER = weights.get("weather", 0.30)
    W_PLACE = weights.get("activity", 0.20)

    # --------------------------------
    # 天氣地點分數
    # --------------------------------
    try:
        weather_score = compute_weather_score(station_key)
    except Exception as e:
        print(f"[Backend] Error calling compute_weather_score: {e}")
        weather_score = 60.0  # 假設的備用分數

    place_score = compute_place_score(lat=lat, lng=lng)

    # --------------------------------
    # 歷史 Match 滿意度 (計算對方給你的平均分數)
    # --------------------------------
    # 查詢與當前用戶相關的所有已確認 Match
    matches = (
        db.query(Match)
        .join(Invite, Match.invite_id == Invite.id)
        .filter(
            Match.status == "confirmed",
            (Match.receiver_id == current_user.id)
            | (Invite.sender_id == current_user.id),
        )
        .options(joinedload(Match.invite))  # 重新確保 invite 關係正確載入
        .all()
    )

    history_score = None
    history_label = "無紀錄"
    success_rate = None
    all_partner_ratings = []
    rated_count = 0

    if matches:
        for m in matches:
            partner_rating = None

            if not m.invite:
                continue

            # 判斷對方是否已評分，如果是，則納入計算
            if m.invite.sender_id == current_user.id:
                # 身份：我是 Sender，檢查 Receiver 是否已評分 (m.receiver_rating)
                if m.receiver_rating is not None:
                    partner_rating = m.receiver_rating
            elif m.receiver_id == current_user.id:
                # 身份：我是 Receiver，檢查 Sender 是否已評分 (m.sender_rating)
                if m.sender_rating is not None:
                    partner_rating = m.sender_rating
            else:
                continue

            if partner_rating is not None:
                all_partner_ratings.append(partner_rating)
                rated_count += 1

        if all_partner_ratings:
            history_score = sum(all_partner_ratings) / len(all_partner_ratings)
            history_label = f"有 {rated_count} 筆紀錄"

            # --------------------------------
            # 最終權重計算 (使用動態權重)
            # --------------------------------
            success_rate = (
                (history_score * W_HISTORY)
                + (weather_score * W_WEATHER)
                + (place_score * W_PLACE)
            )

            success_rate = round(max(0, min(100, success_rate)), 2)
        else:
            history_label = "無紀錄"
            # 如果沒有歷史評分，Success Rate 可以使用一個基於天氣和地點的基線值
            success_rate = (
                (80 * W_HISTORY)  # 假設無歷史時，歷史分數給 80 分
                + (weather_score * W_WEATHER)
                + (place_score * W_PLACE)
            )
            success_rate = round(max(0, min(100, success_rate)), 2)

    # --------------------------------
    # 回傳結果
    # --------------------------------
    return {
        "weather_score": round(weather_score, 2),
        "place_score": round(place_score, 2),
        "history_score": (
            round(history_score, 2) if history_score is not None else 80.0
        ),  # 配合前端顯示無紀錄時的基線
        "history_label": history_label,
        "success_rate": success_rate,
    }
