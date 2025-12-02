from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

# 1. 引入所有的 Router
from user_routes import router as user_router
from place_routes import router as place_router
from weather_map import router as weather_router
from history_routes import router as history_router

app = FastAPI(
    title="Meetro Backend",
    description="Backend API",
    version="1.0",
)

# 2. 自動建立資料表
Base.metadata.create_all(bind=engine)

# 3. CORS 設定
origins = ["http://localhost:8080", "http://127.0.0.1:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. 掛載 Router (關鍵！這一區塊不能少)
app.include_router(user_router)  # 負責 /auth/login, /auth/register
app.include_router(place_router)  # 負責捷運站
app.include_router(weather_router)  # 負責天氣
app.include_router(history_router)  # 負責歷史紀錄


@app.get("/")
def root():
    return {"message": "Meetro Backend is running!"}


@app.get("/api/hello")
def hello():
    return {"message": "Connection Successful"}
