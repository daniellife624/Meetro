from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from backend.database import SessionLocal
from backend.auth import get_current_user
from backend.models import User, Match, Invite, SystemVariable
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


# --------------------------------
# 動態權重讀取函式
# --------------------------------
def get_weights(db: Session) -> dict:
    """從資料庫讀取 SystemVariable 權重，並轉換為 0.0 到 1.0 的浮點數"""
    weights = {}
    configs = db.query(SystemVariable).all()

    if not configs:
        # 如果資料庫為空，返回一個合理的預設值 (必須總和為 1.0)
        return {
            "歷史滿意度": 0.50,
            "天氣影響": 0.30,
            "地點熱門度": 0.20,
        }

    for c in configs:
        # 將 Integer 權重 (0-100) 轉換為 Float (0.0-1.0)
        weights[c.name] = c.weight / 100.0

    return weights


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

    # 讀取動態權重
    weights = get_weights(db)

    # 確保所有權重都存在 (使用 .get() 獲取，若不存在則使用預設值)
    W_HISTORY = weights.get("歷史滿意度", 0.50)
    W_WEATHER = weights.get("天氣影響", 0.30)
    W_PLACE = weights.get("地點熱門度", 0.20)

    # --------------------------------
    # 1. 天氣地點分數
    # --------------------------------
    try:
        weather_score = compute_weather_score(station_key)
    except Exception as e:
        print(f"[Backend] Error calling compute_weather_score: {e}")
        weather_score = 60.0

    place_score = compute_place_score(lat=lat, lng=lng)

    # --------------------------------
    # 2. 歷史 Match 滿意度 (計算對方給你的平均分數)
    # --------------------------------
    matches = (
        db.query(Match)
        .options(joinedload(Match.invite))
        .filter(
            Match.status == "confirmed",
            (Match.receiver_id == current_user.id)
            | (Invite.sender_id == current_user.id),
        )
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

            # 確保 m.invite 存在 (避免在舊紀錄中出錯)
            if not m.invite:
                continue

            # 判斷對方是否已評分，如果是，則納入計算
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
            history_score = sum(all_partner_ratings) / len(all_partner_ratings)
            history_label = f"有 {rated_count} 筆紀錄"

            # --------------------------------
            # 3. 最終權重計算 (使用動態權重)
            # --------------------------------
            success_rate = (
                (history_score * W_HISTORY)
                + (weather_score * W_WEATHER)
                + (place_score * W_PLACE)
            )

            success_rate = round(max(0, min(100, success_rate)), 2)
        else:
            history_label = "無紀錄"
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
