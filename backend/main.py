# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.models import Base
from backend.user_routes import router as user_router
from backend.place_routes import router as place_router

app = FastAPI(
    title="Meetro Backend",
    description="Backend API",
    version="1.0",
)

# 建立資料表
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 之後可以改成前端正式網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載 router
app.include_router(user_router)
app.include_router(place_router)


@app.get("/")
def root():
    return {"message": "Meetro backend is running"}
