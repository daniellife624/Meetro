# backend/services/success_rate_service.py
from sqlalchemy.orm import Session
from backend.models import SystemVariable, Match, User
from backend.database import SessionLocal
from typing import Dict, Any

# 假設您已經有了獲取 SystemVariable 權重和計算各項分數的邏輯


def get_bcms_weights(db: Session) -> Dict[str, float]:
    """獲取當前 BCMS 權重，並轉換為小數 (0.0 - 1.0)"""
    weights = db.query(SystemVariable).all()
    weight_map = {w.name: w.weight / 100.0 for w in weights}

    # 設置預設值以防數據庫為空 (與 init_data.py 保持一致)
    return {
        "history": weight_map.get("歷史滿意度", 0.50),
        "weather": weight_map.get("天氣影響", 0.30),
        "activity": weight_map.get("地點熱門度", 0.20),
    }


def calculate_history_score(db: Session, user_id: int) -> float:
    """計算用戶的歷史滿意度分數 (假設返回 0-100)"""
    # 邏輯：平均所有用戶給這個 user 的評分

    # 找出所有 "receiver_id" 是此 user 的 Match，且 sender 已評分
    matches_as_receiver = (
        db.query(Match)
        .filter(Match.receiver_id == user_id, Match.sender_rating.isnot(None))
        .all()
    )

    # 找出所有 "sender_id" 是此 user 的 Match，且 receiver 已評分
    matches_as_sender = (
        db.query(Match)
        .filter(Match.sender_id == user_id, Match.receiver_rating.isnot(None))
        .all()
    )

    all_ratings = []
    # 收集作為接收方時，發送方給的評分
    all_ratings.extend(
        [m.sender_rating for m in matches_as_receiver if m.sender_rating is not None]
    )
    # 收集作為發送方時，接收方給的評分
    all_ratings.extend(
        [m.receiver_rating for m in matches_as_sender if m.receiver_rating is not None]
    )

    if not all_ratings:
        return 80.0  # 假設沒有歷史評分時給予一個預設值 (例如 80 分)

    return sum(all_ratings) / len(all_ratings)


def calculate_simulated_success_rate(db: Session, user_id: int) -> float:
    """
    計算用戶的模擬成功率 (Simulated Success Rate)
    返回 0-100 的浮點數百分比。
    """
    # 1. 獲取權重
    weights = get_bcms_weights(db)

    # 2. 獲取分數 (使用模擬/簡化分數，因為我們沒有實時天氣和地點數據)
    history_score = calculate_history_score(db, user_id)

    # 🚨 模擬分數 (請根據您的實際項目調整或使用您實際計算的分數)
    # 假設這兩個分數與用戶本身無關，是取決於邀約發生的時間地點
    weather_score = 90.0
    activity_score = 85.0

    # 3. 應用 BCMS 權重公式
    success_rate = (
        weights["history"] * history_score
        + weights["weather"] * weather_score
        + weights["activity"] * activity_score
    )

    return round(success_rate, 1)  # 返回一位小數
