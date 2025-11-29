from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base
from user_routes import router as user_router
from place_routes import router as place_router

from weather_map import router as weather_router

app = FastAPI(
    title="Meetro Backend",
    description="Backend API",
    version="1.0",
)

# [暫時註解] 自動建立資料表
# Base.metadata.create_all(bind=engine)

# CORS 設定 (保持開啟，前端才能連)
origins = ["http://localhost:8080", "http://127.0.0.1:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [暫時註解] 掛載真實功能的 router (因為它們需要 DB)
# app.include_router(user_router)
# app.include_router(place_router)
app.include_router(weather_router)
# --- 保留測試用的 Mock API ---


@app.get("/")
def root():
    return {"message": "Meetro backend is running (Mock Mode)"}


@app.get("/api/hello")
def hello():
    return {"message": "恭喜！前端成功連線到後端了 🎉"}


@app.get("/api/stations/{station_key}")
def get_station_info(station_key: str):
    # 模擬資料庫內容
    mock_db = {
        "songshan": {
            "weather": "晴朗 28°C (來自後端)",
            "attractions": ["饒河街夜市", "慈祐宮", "彩虹橋"],
        },
        "gongguan": {
            "weather": "多雲 26°C (來自後端)",
            "attractions": ["台灣大學", "水源市場", "寶藏巖"],
        },
        "xindian": {
            "weather": "陰天 24°C (來自後端)",
            "attractions": ["碧潭吊橋", "和美山步道"],
        },
    }

    data = mock_db.get(station_key)

    if data:
        return data
    else:
        return {"weather": "未知天氣 (後端無資料)", "attractions": ["暫無景點資料"]}
