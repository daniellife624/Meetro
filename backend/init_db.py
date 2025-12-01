# backend/init_db.py
from database import engine, Base

# 必須引入 models，Base 才知道要建哪些表
from models import User

# from models import Station, Attraction, Invite, Match, Ema, SystemVariable


def init_db():
    print("正在建立資料庫表格...")
    # 這行指令會根據 models.py 的定義，在資料庫中建立所有表格
    Base.metadata.create_all(bind=engine)
    print("資料庫初始化完成！")


if __name__ == "__main__":
    init_db()
