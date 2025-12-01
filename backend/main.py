from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

# 引入功能 Router
from user_routes import router as user_router
from place_routes import router as place_router
from weather_map import router as weather_router

# from history_routes import router as history_router

app = FastAPI(title="Meetro Backend", version="1.0")

Base.metadata.create_all(bind=engine)

# CORS 設定 (重要！確保前端能連)
origins = ["http://localhost:8080", "http://127.0.0.1:8080", "*"]  # 開發階段方便測試

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載 Router
app.include_router(user_router)
app.include_router(place_router)
app.include_router(weather_router)
# app.include_router(history_router)


@app.get("/")
def root():
    return {"message": "Meetro Backend is running with SQLite!"}


@app.get("/api/hello")
def hello():
    return {"message": "Connection Successful"}
