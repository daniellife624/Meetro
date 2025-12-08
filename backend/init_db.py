# backend/init_db.py
from backend.database import engine, SessionLocal, Base
from backend.models import Station, Attraction, User

# 定義初始資料 (松山新店線)
INITIAL_DATA = {
    "songshan": {
        "name": "松山",
        "attractions": ["饒河街夜市", "松山慈祐宮", "彩虹橋", "五分埔"],
    },
    "nanjingsanmin": {
        "name": "南京三民",
        "attractions": ["京華城舊址", "民生社區", "偶戲館"],
    },
    "taipeiarena": {
        "name": "台北小巨蛋",
        "attractions": ["臺北小巨蛋", "松山運動中心", "臺北田徑場"],
    },
    "nanjingfuxing": {"name": "南京復興", "attractions": ["遼寧夜市", "兄弟大飯店"]},
    "songjiangnanjing": {
        "name": "松江南京",
        "attractions": ["四平陽光商圈", "袖珍博物館", "伊通公園"],
    },
    "zhongshan": {
        "name": "中山",
        "attractions": ["心中山線形公園", "光點台北", "赤峰街", "當代藝術館"],
    },
    "beimen": {
        "name": "北門",
        "attractions": ["北門(承恩門)", "台北郵局", "撫臺街洋樓", "相機街"],
    },
    "ximen": {
        "name": "西門",
        "attractions": ["西門紅樓", "臺北市電影主題公園", "萬年大樓", "西本願寺"],
    },
    "xiaonanmen": {
        "name": "小南門",
        "attractions": ["臺北植物園", "國立歷史博物館", "郵政博物館"],
    },
    "chiangkaishekmemorialhall": {
        "name": "中正紀念堂",
        "attractions": ["中正紀念堂", "國家戲劇院", "國家音樂廳", "南門市場"],
    },
    "guting": {
        "name": "古亭",
        "attractions": ["紀州庵文學森林", "客家文化主題公園", "師大校園"],
    },
    "taipowerbuilding": {
        "name": "台電大樓",
        "attractions": ["師大夜市", "寶藏巖", "客家文化園區"],
    },
    "gongguan": {
        "name": "公館",
        "attractions": ["國立臺灣大學", "水源市場", "自來水博物館", "公館商圈"],
    },
    "wanlong": {"name": "萬隆", "attractions": ["景美溪河濱公園", "花木批發市場"]},
    "jingmei": {"name": "景美", "attractions": ["景美夜市", "仙跡岩步道", "集應廟"]},
    "dapinglin": {
        "name": "大坪林",
        "attractions": ["景美橋", "慈濟醫院", "十四張歷史公園"],
    },
    "qizhang": {"name": "七張", "attractions": ["裕隆城", "誠品生活", "原野公園"]},
    "xiaobitan": {
        "name": "小碧潭",
        "attractions": ["IKEA 新店店", "京站小碧潭", "陽光運動公園"],
    },
    "xindiandistrictoffice": {
        "name": "新店區公所",
        "attractions": ["馬公友誼公園", "新店圖書館"],
    },
    "xindian": {
        "name": "新店",
        "attractions": ["碧潭吊橋", "和美山步道", "新店老街", "碧潭風景區"],
    },
}


def init_db():
    print("正在連接資料庫...")
    # 1. 建立表格
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("正在檢查並寫入初始資料...")

        for key, data in INITIAL_DATA.items():
            # 檢查站點是否存在
            station = db.query(Station).filter(Station.key == key).first()

            if not station:
                print(f"新增站點: {data['name']} ({key})")
                # 建立站點 (經緯度暫時填 0，之後可透過 Google API 更新或手動補)
                station = Station(
                    key=key,
                    name_zh=data["name"],
                    line_code="G",
                    latitude=0,
                    longitude=0,
                )
                db.add(station)
                db.commit()
                db.refresh(station)

            # 檢查該站點是否已有景點，若無則新增
            if not station.attractions:
                for attr_name in data["attractions"]:
                    print(f"  - 新增景點: {attr_name}")
                    db.add(Attraction(name=attr_name, station_id=station.id))
                db.commit()

        print("資料庫初始化完成！已寫入捷運站與景點資料。")

    except Exception as e:
        print(f"初始化失敗: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
