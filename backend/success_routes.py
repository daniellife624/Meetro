from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import get_current_user
from backend.models import User, Match
from backend.weather_map import compute_weather_score, compute_place_score

router = APIRouter(prefix="/success", tags=["success"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/estimate")
def estimate_success_rate(
    station_key: str = Query(..., description="捷運站 key，例如 ximen"),
    lat: float = Query(..., description="地點緯度"),
    lng: float = Query(..., description="地點經度"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    使用 天氣分數 + Google 評分 + 歷史滿意度（若有）
    估算此次邀約成功率。

    若沒有歷史紀錄 → success_rate = None
    """

    # --------------------------------
    # 1. 天氣地點分數
    # --------------------------------
    weather_score = compute_weather_score(station_key)
    place_score = compute_place_score(lat=lat, lng=lng)

    # --------------------------------
    # 2. 歷史 Match 滿意度
    # --------------------------------
    matches = (
        db.query(Match)
        .filter(
            Match.receiver_id == current_user.id,
            Match.satisfaction_score.isnot(None)
        )
        .all()
    )

    if matches:
        raw_scores = [m.satisfaction_score for m in matches]
        avg_raw = sum(raw_scores) / len(raw_scores)   # 平均 1~5
        history_score = (avg_raw / 5.0) * 100         # 轉成 0~100
        history_label = "有紀錄"
        success_rate = (
            weather_score * 0.30 +
            place_score * 0.20 +
            history_score * 0.50
        )
        success_rate = round(max(0, min(100, success_rate)), 2)

    else:
        # 無紀錄時：不進行權重計算
        history_score = None
        history_label = "無紀錄"
        success_rate = None

    # --------------------------------
    # 3. 回傳結果
    # --------------------------------
    return {
        "weather_score": round(weather_score, 2),
        "place_score": round(place_score, 2),
        "history_score": round(history_score, 2) if history_score is not None else None,
        "history_label": history_label,
        "success_rate": success_rate,
    }