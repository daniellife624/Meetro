from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.models import Base

# 1. 引入所有的 Router
from backend.user_routes import router as user_router
from backend.place_routes import router as place_router
from backend.weather_routes import router as weather_router
from backend.history_routes import router as history_router
from backend.ema_routes import router as ema_router
from backend.invite_routes import router as invite_router
from backend.success_routes import router as success_router


app = FastAPI(
    title="Meetro Backend",
    description="Backend API",
    version="1.0",
)

# 自動建立資料表
Base.metadata.create_all(bind=engine)

# CORS 設定
origins = ["http://localhost:8080", "http://127.0.0.1:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. 掛載 Router
app.include_router(user_router)  # 負責 /auth/login, /auth/register
app.include_router(place_router)  # 負責捷運站
app.include_router(weather_router)  # 負責天氣
app.include_router(history_router)  # 負責歷史紀錄
app.include_router(ema_router)  # 負責繪馬牆
app.include_router(invite_router)  # 負責邀約
app.include_router(success_router)  # 計算成功率模擬


@app.get("/")
def root():
    return {"message": "Meetro Backend is running!"}


@app.get("/api/hello")
def hello():
    return {"message": "Connection Successful"}
