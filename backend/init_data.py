# backend/init_data.py (完整整合版本)

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models import (
    Station,
    Attraction,
    User,
    SystemVariable,
)

# -----------------------------------
# 1. 靜態資料定義 (松山新店線全線，包含經緯度)
# -----------------------------------
# 座標來源: Google Maps / 各大開放資料 (用於模擬地點分數和 Google API 查詢)
STATIONS_FULL_DATA = {
    "songshan": {
        "name": "松山",
        "line_code": "G",
        "lat": 25.05047,
        "lng": 121.55431,
        "attractions": ["饒河街夜市", "松山慈祐宮", "彩虹橋", "五分埔"],
    },
    "nanjingsanmin": {
        "name": "南京三民",
        "line_code": "G",
        "lat": 25.05200,
        "lng": 121.55400,
        "attractions": ["京華城舊址", "民生社區", "偶戲館"],
    },
    "taipeiarena": {
        "name": "台北小巨蛋",
        "line_code": "G",
        "lat": 25.05190,
        "lng": 121.54921,
        "attractions": ["臺北小巨蛋", "松山運動中心", "臺北田徑場"],
    },
    "nanjingfuxing": {
        "name": "南京復興",
        "line_code": "G",
        "lat": 25.05273,
        "lng": 121.54326,
        "attractions": ["遼寧夜市", "兄弟大飯店"],
    },
    "songjiangnanjing": {
        "name": "松江南京",
        "line_code": "G",
        "lat": 25.05216,
        "lng": 121.53606,
        "attractions": ["四平陽光商圈", "袖珍博物館", "伊通公園"],
    },
    "zhongshan": {
        "name": "中山",
        "line_code": "G",
        "lat": 25.05255,
        "lng": 121.52734,
        "attractions": ["心中山線形公園", "光點台北", "赤峰街", "當代藝術館"],
    },
    "beimen": {
        "name": "北門",
        "line_code": "G",
        "lat": 25.04899,
        "lng": 121.51347,
        "attractions": ["北門(承恩門)", "台北郵局", "撫臺街洋樓", "相機街"],
    },
    "ximen": {
        "name": "西門",
        "line_code": "G",
        "lat": 25.04470,
        "lng": 121.50764,
        "attractions": ["西門紅樓", "臺北市電影主題公園", "萬年大樓", "西本願寺"],
    },
    "xiaonanmen": {
        "name": "小南門",
        "line_code": "G",
        "lat": 25.03541,
        "lng": 121.50974,
        "attractions": ["臺北植物園", "國立歷史博物館", "郵政博物館"],
    },
    "chiangkaishekmemorialhall": {
        "name": "中正紀念堂",
        "line_code": "G",
        "lat": 25.03565,
        "lng": 121.51909,
        "attractions": ["中正紀念堂", "國家戲劇院", "國家音樂廳", "南門市場"],
    },
    "guting": {
        "name": "古亭",
        "line_code": "G",
        "lat": 25.03155,
        "lng": 121.52885,
        "attractions": ["紀州庵文學森林", "客家文化主題公園", "師大校園"],
    },
    "taipowerbuilding": {
        "name": "台電大樓",
        "line_code": "G",
        "lat": 25.02347,
        "lng": 121.53239,
        "attractions": ["師大夜市", "寶藏巖", "客家文化園區"],
    },
    "gongguan": {
        "name": "公館",
        "line_code": "G",
        "lat": 25.01258,
        "lng": 121.53621,
        "attractions": ["國立臺灣大學", "水源市場", "自來水博物館", "公館商圈"],
    },
    "wanlong": {
        "name": "萬隆",
        "line_code": "G",
        "lat": 25.00067,
        "lng": 121.53622,
        "attractions": ["景美溪河濱公園", "花木批發市場"],
    },
    "jingmei": {
        "name": "景美",
        "line_code": "G",
        "lat": 24.99464,
        "lng": 121.54010,
        "attractions": ["景美夜市", "仙跡岩步道", "集應廟"],
    },
    "dapinglin": {
        "name": "大坪林",
        "line_code": "G",
        "lat": 24.98661,
        "lng": 121.54512,
        "attractions": ["景美橋", "慈濟醫院", "十四張歷史公園"],
    },
    "qizhang": {
        "name": "七張",
        "line_code": "G",
        "lat": 24.98150,
        "lng": 121.54751,
        "attractions": ["裕隆城", "誠品生活", "原野公園"],
    },
    "xiaobitan": {
        "name": "小碧潭",
        "line_code": "G",
        "lat": 24.97761,
        "lng": 121.53957,
        "attractions": ["IKEA 新店店", "京站小碧潭", "陽光運動公園"],
    },
    "xindiandistrictoffice": {
        "name": "新店區公所",
        "line_code": "G",
        "lat": 24.97547,
        "lng": 121.54226,
        "attractions": ["馬公友誼公園", "新店圖書館"],
    },
    "xindian": {
        "name": "新店",
        "line_code": "G",
        "lat": 24.96860,
        "lng": 121.53819,
        "attractions": ["碧潭吊橋", "和美山步道", "新店老街", "碧潭風景區"],
    },
}

# 預設的 BCMS 權重配置 (確保總和為 100%)
DEFAULT_BCMS_CONFIGS = [
    {
        "name": "歷史滿意度",
        "weight": 50,
        "rule_desc": "根據歷史使用者的回饋評分進行動態調整，佔總機率的 50%。",
    },
    {
        "name": "天氣影響",
        "weight": 30,
        "rule_desc": "若當日降雨機率過高，戶外站點權重降低，佔總機率的 30%。",
    },
    {
        "name": "地點熱門度",
        "weight": 20,
        "rule_desc": "根據周邊景點數量與熱門程度進行加權計算，佔總機率的 20%。",
    },
]
# -----------------------------------
# 2. 初始化函式
# -----------------------------------


def init_stations_and_attractions(db: Session):
    """初始化站點和景點資料"""
    print("--- 開始初始化捷運站與景點資料 ---")
    if db.query(Station).first():
        print("資料庫中已存在站點資料，跳過站點初始化。")
        return

    for key, data in STATIONS_FULL_DATA.items():
        # 建立站點
        station = Station(
            key=key,
            name_zh=data["name"],
            line_code=data["line_code"],
            latitude=data["lat"],
            longitude=data["lng"],
        )
        db.add(station)
        db.commit()
        db.refresh(station)
        print(f"已新增站點: {data['name']} ({key})")

        # 寫入景點
        for attr_name in data["attractions"]:
            db.add(Attraction(name=attr_name, station_id=station.id))

    db.commit()
    print("--- 捷運站與景點資料初始化完成 ---")


def init_system_variables(db: Session):  # 函式名稱更新
    """初始化系統變數 (BCMS 參數)"""
    if db.query(SystemVariable).first():  # 使用 SystemVariable
        print("--- 系統變數已存在，跳過初始化 ---")
        return

    print("--- 開始初始化系統變數 ---")
    for config_data in DEFAULT_BCMS_CONFIGS:
        db_config = SystemVariable(
            name=config_data["name"],
            weight=config_data["weight"],
            rule_desc=config_data["rule_desc"],
        )
        db.add(db_config)

    db.commit()
    print("--- 系統變數初始化完成 ---")


def init_users(db: Session):
    """初始化測試用戶 (保持與之前一致)"""
    # 這裡可以加入測試用戶邏輯
    pass  # 假設您有單獨的用戶初始化邏輯，這裡先保持不變


# -----------------------------------
# 3. 主執行區塊
# -----------------------------------

if __name__ == "__main__":
    print("正在連接資料庫...")
    # 確保所有 Model 都被載入，並建立資料表
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    init_stations_and_attractions(db)
    init_system_variables(db)  # BCMS 參數
    init_users(db)  # 用戶初始化 (如果需要)
    db.close()
    print("初始化腳本運行結束。")
