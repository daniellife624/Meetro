# backend/bcms_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from backend.database import SessionLocal
from backend.models import SystemVariable

router = APIRouter(prefix="/api/bcms", tags=["bcms"])


# --- Pydantic Schemas ---
class VariableIn(BaseModel):
    name: str
    weight: int
    rule: str


class VariableOut(BaseIn):
    id: int
    name: str
    weight: int
    rule: str

    model_config = {"from_attributes": True}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------
#     API Endpoints
# -----------------------------------


@router.get("/config", response_model=List[VariableOut])
def get_all_config(db: Session = Depends(get_db)):
    """獲取所有權重配置"""
    configs = db.query(SystemVariable).all()

    results = []
    for c in configs:
        results.append(
            {
                "id": c.id,
                "name": c.name,
                "weight": c.weight,
                "rule": c.rule_desc,
            }
        )
    return results


@router.post("/config/save")
def save_config(variables: List[VariableIn], db: Session = Depends(get_db)):
    """保存或更新所有權重配置 (覆蓋模式)"""

    # 刪除舊數據
    db.query(SystemVariable).delete()

    # 寫入新數據
    for v in variables:
        if v.weight < 0 or v.weight > 100:
            raise HTTPException(status_code=400, detail="權重必須介於 0 到 100 之間")

        # 寫入 SystemVariable
        new_config = SystemVariable(
            name=v.name,
            weight=v.weight,  # 直接寫入 Integer 權重
            rule_desc=v.rule,  # 寫入 Model 的 rule_desc 欄位
        )
        db.add(new_config)

    db.commit()
    return {"message": "參數配置保存成功"}
