# backend/init_data.py

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Base, Station

# 1. 初始化資料 (綠線部分站點)
STATIONS_TO_ADD = [
    {"key": "songshan", "name_zh": "松山", "line_code": "G"},
    {"key": "nanjingfuxing", "name_zh": "南京復興", "line_code": "G"},
    {"key": "gongguan", "name_zh": "公館", "line_code": "G"},
    {"key": "xindian", "name_zh": "新店", "line_code": "G"},
    # 如果需要，可以在這裡加入其他站點
]


def init_stations(db: Session):
    print("--- 開始初始化捷運站資料 (init_data.py) ---")

    # 檢查是否已存在任何站點，如果存在則跳過
    if db.query(Station).first():
        print("資料庫中已存在站點資料，跳過初始化。")
        return

    # 寫入站點
    for data in STATIONS_TO_ADD:
        station = Station(
            key=data["key"],
            name_zh=data["name_zh"],
            line_code=data["line_code"],
        )
        db.add(station)
        print(f"已新增站點: {data['name_zh']} ({data['key']})")

    db.commit()
    print("--- 捷運站資料初始化完成 ---")


if __name__ == "__main__":
    # 確保所有 Model 都被載入，並建立資料表
    # 🚨 注意：這將會在 /tmp/meetro.db 建立表格
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    init_stations(db)
    db.close()
