# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 設定 SQLite 資料庫檔案位置
# 檔案會產生在 backend 目錄下的 meetro.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./meetro.db"

# 2. 建立 Engine
# check_same_thread: False 是 SQLite 專用的設定，允許在多執行緒中使用
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 建立 Session 工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 宣告 Base，供 models.py 繼承
Base = declarative_base()
