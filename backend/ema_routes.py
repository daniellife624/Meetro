# backend/ema_routes.py
# 定義 GET/POST 的邏輯
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from database import SessionLocal
from models import Ema, Station, User
from auth import get_current_user
import schemas

router = APIRouter(prefix="/api/emas", tags=["emas"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. 取得特定站點的繪馬牆
@router.get("/{station_key}", response_model=List[schemas.EmaOut])
def get_station_emas(station_key: str, db: Session = Depends(get_db)):
    # 先找出站點 ID
    station = db.query(Station).filter(Station.key == station_key.lower()).first()

    if not station:
        return []  # 如果站點不存在，回傳空列表

    # 查詢該站點的繪馬，並預先載入 User 資料 (為了拿名字)
    emas = (
        db.query(Ema)
        .options(joinedload(Ema.user))
        .filter(Ema.station_id == station.id)
        .order_by(Ema.created_at.desc())  # 新的在上面
        .all()
    )

    # 轉換格式回傳
    results = []
    for ema in emas:
        results.append(
            {
                "id": ema.id,
                "userName": ema.user.name if ema.user else "匿名",
                "location": ema.location_text,
                "content": ema.content,
                "photoUrl": ema.photo_url,
                "date": ema.created_at.strftime("%Y/%m/%d") if ema.created_at else "",
            }
        )

    return results


# 2. 新增繪馬 (需登入)
@router.post("", response_model=schemas.EmaOut)
def create_ema(
    ema_in: schemas.EmaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 找出站點
    station = (
        db.query(Station).filter(Station.key == ema_in.station_key.lower()).first()
    )
    if not station:
        raise HTTPException(status_code=404, detail="站點不存在")

    # 建立繪馬
    new_ema = Ema(
        user_id=current_user.id,
        station_id=station.id,
        content=ema_in.content,
        location_text=ema_in.location,
        photo_url=ema_in.photo_url,
        created_at=datetime.now(),
    )

    db.add(new_ema)
    db.commit()
    db.refresh(new_ema)

    # 回傳格式
    return {
        "id": new_ema.id,
        "userName": current_user.name,
        "location": new_ema.location_text,
        "content": new_ema.content,
        "photoUrl": new_ema.photo_url,
        "date": new_ema.created_at.strftime("%Y/%m/%d"),
    }
