# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================
# 選項 1: PostgreSQL (正式環境推薦)
# ==========================================
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://meetro_user:meetro_password@db:5432/meetro_db"

# ==========================================
# 選項 2: SQLite (本機測試用)
# ==========================================
# SQLALCHEMY_DATABASE_URL = "sqlite:///./meetro.db"

# ==========================================
# 目前狀態: Mock Mode (無資料庫)
# ==========================================

# 1. 必須定義 Base，否則 models.py 會報錯
Base = declarative_base()

# 2. 定義空的 engine 和 SessionLocal
# 這樣其他檔案 (如 main.py) 嘗試 import 時才不會找不到變數
# 等確定資料庫後，再把下面的 None 替換成 create_engine(...)
engine = None
SessionLocal = None

# 未來啟用資料庫時的參考寫法 (請保留註解):
# if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
#     engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# else:
#     engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
