# backend/bcms_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

from backend.database import SessionLocal
from backend.models import SystemVariable
from backend.auth import get_current_user

# 🚨 實際專案中，這裡應該有 Admin 權限檢查，但為了功能測試，先省略

router = APIRouter(prefix="/api/bcms", tags=["bcms"])


# --- Pydantic Schemas ---
# 用於前端提交數據的輸入模型
class VariableIn(BaseModel):
    name: str = Field(..., description="參數名稱")
    weight: int = Field(..., ge=0, le=100, description="權重值 (0-100 範圍)")
    rule: str = Field(..., description="規則描述 (對應 SystemVariable.rule_desc)")


# 用於 API 輸出的數據模型
class VariableOut(BaseModel):
    id: int
    name: str
    weight: int
    rule: str  # 對應 SystemVariable.rule_desc

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
    """獲取所有權重配置 (SystemVariable)"""
    configs = db.query(SystemVariable).all()

    # 轉換數據格式以匹配前端期待的 'rule' 欄位
    results = []
    for c in configs:
        results.append(
            {
                "id": c.id,
                "name": c.name,
                "weight": c.weight,  # 已經是 0-100 的整數
                "rule": c.rule_desc,  # 將後端的 rule_desc 映射到前端的 rule
            }
        )
    return results


@router.post("/config/save")
def save_config(variables: List[VariableIn], db: Session = Depends(get_db)):
    """保存或更新所有權重配置 (覆蓋模式)"""

    # 檢查總和是否為 100
    if sum(v.weight for v in variables) != 100:
        raise HTTPException(
            status_code=400, detail="所有參數的權重總和必須剛好等於 100。"
        )

    # 刪除舊數據 (覆蓋模式)
    db.query(SystemVariable).delete()

    # 寫入新數據
    for v in variables:
        new_config = SystemVariable(
            name=v.name,
            weight=v.weight,  # 直接寫入 Integer 權重
            rule_desc=v.rule,  # 寫入 rule_desc
        )
        db.add(new_config)

    db.commit()
    return {"message": "參數配置保存成功"}
