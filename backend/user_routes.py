# backend/user_routes.py
# 註冊 / 登入 / 取得自己資料 / admin 範例
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import schemas
from backend.database import SessionLocal
from backend.models import User
from backend.security import hash_password, verify_password
from backend.auth import create_access_token, get_current_user, get_admin_user

router = APIRouter(prefix="/auth", tags=["auth"])

# 也可以改用 auth.get_db，但這裡再寫一份也 OK
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # ✅ 驗證 Email 唯一性
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="此 Email 已被註冊")

    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")

    # JWT 裡放 user_id / email / role
    token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer"}


# ✅ 需要登入才能看的 API
@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ 只有 admin 能用的 API 範例
@router.get("/admin/overview")
def admin_only_view(admin: User = Depends(get_admin_user)):
    return {"message": f"歡迎管理員 {admin.email}"}
