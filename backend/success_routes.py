from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from backend.database import SessionLocal
from backend.auth import get_current_user
from backend.models import User, Match, Invite
from backend.weather_routes import compute_weather_score, compute_place_score

router = APIRouter(prefix="/api/success", tags=["success"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    只要對方已評分，即可納入歷史滿意度計算。
    計算公式：天氣分數*30% + 地點分數*20% + 歷史滿意度*50%
    """

    # --------------------------------
    # 1. 天氣地點分數
    # --------------------------------
    try:
        # 呼叫 weather_routes 裡定義的工具函式
        weather_score = compute_weather_score(station_key)
    except Exception as e:
        print(f"[Backend] Error calling compute_weather_score: {e}")
        # 如果天氣 API 失敗，給予中性分數 (當作陰天)
        weather_score = 60.0

    place_score = compute_place_score(lat=lat, lng=lng)

    # --------------------------------
    # 2. 歷史 Match 滿意度 (計算對方給你的平均分數)
    # --------------------------------
    # 查詢該使用者所有狀態為 'confirmed' 且雙方都已評分的 Match 紀錄
    matches = (
        db.query(Match)
        .options(joinedload(Match.invite))
        .filter(
            # 必須是已確認的 Match
            Match.status == "confirmed",
            # 必須是雙方都已評分的 Match
            (Match.receiver_id == current_user.id)
            | (Invite.sender_id == current_user.id),
        )
        .all()
    )

    history_score = None
    history_label = "無紀錄"
    success_rate = None
    all_partner_ratings = []
    rated_count = 0  # 紀錄有效評分次數

    if matches:
        for m in matches:
            # 判斷對方是否已評分，如果是，則納入計算
            partner_rating = None

            if m.invite.sender_id == current_user.id:
                # 身份：我是 Sender，檢查 Receiver 是否已評分
                if m.receiver_rating is not None:
                    partner_rating = m.receiver_rating
            elif m.receiver_id == current_user.id:
                # 身份：我是 Receiver，檢查 Sender 是否已評分
                if m.sender_rating is not None:
                    partner_rating = m.sender_rating
            else:
                continue

            if partner_rating is not None:
                all_partner_ratings.append(partner_rating)
                rated_count += 1

        if all_partner_ratings:
            # 計算歷史滿意度的平均值 (0-100 分制)
            history_score = sum(all_partner_ratings) / len(all_partner_ratings)
            history_label = f"有 {rated_count} 筆紀錄"

            # --------------------------------
            # 3. 最終權重計算 (預測下次邀約成功率)
            # --------------------------------
            # 權重：歷史滿意度 50% + 天氣 30% + 地點 20%
            success_rate = (
                (history_score * 0.50) + (weather_score * 0.30) + (place_score * 0.20)
            )

            # 確保結果介於 0 到 100 之間
            success_rate = round(max(0, min(100, success_rate)), 2)
        else:
            history_label = "有紀錄，但評分不完整"
            success_rate = None

    # --------------------------------
    # 4. 回傳結果
    # --------------------------------
    return {
        "weather_score": round(weather_score, 2),
        "place_score": round(place_score, 2),
        "history_score": round(history_score, 2) if history_score is not None else None,
        "history_label": history_label,
        "success_rate": success_rate,
    }
