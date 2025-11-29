# backend/user_routes.py
from fastapi import APIRouter, Depends, HTTPException

# from sqlalchemy.orm import Session

import schemas
from database import SessionLocal
from models import User
from security import hash_password, verify_password
from auth import create_access_token, get_current_user, get_admin_user

router = APIRouter(prefix="/auth", tags=["auth"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="此 Email 已被註冊")

    # 建立使用者
    # 注意：資料庫欄位是 'name'，前端傳來的 schema 可能是 'username'
    # 我們暫時將 username 的值存入 name，或者你需要去 update schemas.py
    user = User(
        email=user_in.email,
        name=user_in.username,  # 將 username 存入 name 欄位
        hashed_password=hash_password(user_in.password),
        role="user",
        # gender 與 birthday 若 schema 有傳入可在此加入，若無則為 null
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    # 驗證帳號與密碼
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")

    # 簽發 JWT
    # 這裡把 role 放進去，前端解碼後可以用來判斷身分
    token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer"}


# 需要登入才能看的 API
@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# 只有 admin 能用的 API
@router.get("/admin/overview")
def admin_only_view(admin: User = Depends(get_admin_user)):
    return {"message": f"歡迎管理員 {admin.email}"}
