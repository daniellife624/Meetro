from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import backend.schemas
from backend.database import SessionLocal
from backend.models import User
from backend.security import verify_password, hash_password
from backend.auth import (
    create_access_token,
    get_current_user,
    get_admin_user,
    ROLE_USER,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 註冊 API
@router.post("/register", response_model=backend.schemas.UserOut)
def register(user_in: backend.schemas.UserCreate, db: Session = Depends(get_db)):
    password_bytes = user_in.password.encode("utf-8")
    # 🚨 輸出實際接收到的密碼長度（以 bytes 計算）
    print(f"DEBUG: Received password length (bytes): {len(password_bytes)}")
    print(f"DEBUG: Password start (first 10 chars): {user_in.password[:10]}")
    # 1. 檢查 Email 是否存在
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="此 Email 已被註冊")

    # 2. 建立使用者
    user = User(
        email=user_in.email,
        name=user_in.username,  # 對應 schemas 的 username 到 models 的 name
        hashed_password=hash_password(user_in.password),
        role=ROLE_USER,
        gender=user_in.gender,
        birthday=user_in.birthday,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 登入 API
@router.post("/login", response_model=backend.schemas.Token)
def login(user_in: backend.schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. 查詢使用者
    user = db.query(User).filter(User.email == user_in.email).first()

    # 2. 驗證帳密
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # 使用 401 比較標準
            detail="帳號或密碼錯誤",
        )

    # 3. 簽發 JWT
    token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer"}


# 取得個人資料 API
@router.get("/me", response_model=backend.schemas.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# 管理員測試 API
@router.get("/admin/overview")
def admin_only_view(admin: User = Depends(get_admin_user)):
    return {"message": f"歡迎管理員 {admin.email}"}
