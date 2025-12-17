import os
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse

# 引入 DB 相關模組
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Station

# 建立 Router
router = APIRouter(prefix="/api", tags=["weather_map"])

# -----------------------------------
#         設定與常數
# -----------------------------------
CWA_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
CWA_API_KEY = "CWA-624BB740-DC7B-48E2-9002-B077B72CB174"

GOOGLE_API_KEY = "AIzaSyAtF8UQRBtvHLVok_s7h2ItjLs0gaOFrqs"
GOOGLE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

STATION_LOCATION_MAP = {
    "songshan": "臺北市",
    "nanjingsanmin": "臺北市",
    "taipeiarena": "臺北市",
    "nanjingfuxing": "臺北市",
    "songjiangnanjing": "臺北市",
    "zhongshan": "臺北市",
    "beimen": "臺北市",
    "ximen": "臺北市",
    "xiaonanmen": "臺北市",
    "chiangkaishekmemorialhall": "臺北市",
    "guting": "臺北市",
    "taipowerbuilding": "臺北市",
    "gongguan": "臺北市",
    "wanlong": "臺北市",
    "jingmei": "臺北市",
    "dapinglin": "新北市",
    "qizhang": "新北市",
    "xiaobitan": "新北市",
    "xindiandistrictoffice": "新北市",
    "xindian": "新北市",
}


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------
#         工具函式
# -----------------------------------
def fetch_cwa_wx(location_name: str, retries: int = 1, timeout: int = 5) -> Dict:
    token = os.environ.get("CWA_API_KEY") or CWA_API_KEY
    params = {
        "Authorization": token,
        "format": "JSON",
        "locationName": location_name,
        "elementName": "Wx,MinT,MaxT",
    }

    print(f"[Backend] 正在查詢氣象局:{location_name}...")

    for attempt in range(retries + 1):
        try:
            resp = requests.get(CWA_URL, params=params, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
        except:
            time.sleep(0.5)
    return {}


def parse_weather_info(cwa_data: Dict) -> str:
    """解析氣象局回傳的 JSON"""
    try:
        if not cwa_data or "records" not in cwa_data:
            return "暫無資料 (連線異常)"

        locations = cwa_data["records"]["location"]
        if not locations:
            return "查無此縣市資料"

        weather_elements = locations[0]["weatherElement"]

        wx = ""  # 天氣現象
        min_t = ""  # 最低溫
        max_t = ""  # 最高溫

        # 氣象局資料是預報列表，我們取第一個(最近的時段)
        for el in weather_elements:
            time_slot = el["time"][0]
            val = time_slot["parameter"]["parameterName"]

            if el["elementName"] == "Wx":
                wx = val
            elif el["elementName"] == "MinT":
                min_t = val
            elif el["elementName"] == "MaxT":
                max_t = val

        if wx and min_t and max_t:
            return f"{wx}，氣溫 {min_t}-{max_t}°C"
        return wx if wx else "資料不完整"

    except Exception as e:
        print(f"[Backend] Parse Error: {e}")
        return "解析失敗"


# -----------------------------------
#   API Endpoints
# -----------------------------------
@router.get("/stations/{station_key}")
def get_station_info(
    station_key: str, db: Session = Depends(get_db)  # 注入資料庫 Session
):
    """首頁：取得站點天氣與景點"""

    print(f"[API] 查詢站點: {station_key}")

    # 查詢資料庫取得景點
    # 先找站點
    station = db.query(Station).filter(Station.key == station_key.lower()).first()

    attractions_list = []
    if station:
        # 透過關聯取得景點 (models.py 裡有定義 relationship)
        attractions_list = [attr.name for attr in station.attractions]
    else:
        attractions_list = ["(資料庫中無此站點資料)"]

    # 取得天氣
    city = STATION_LOCATION_MAP.get(station_key.lower(), "臺北市")
    cwa_data = fetch_cwa_wx(city)
    weather_str = parse_weather_info(cwa_data)

    return {
        "key": station_key,
        "weather": weather_str,
        "attractions": attractions_list,  # 回傳資料庫撈到的列表
    }


@router.get("/google/place-info")
def get_place_info(lat: float = Query(...), lng: float = Query(...)):
    """SenderView：點擊地圖取得地點資訊"""

    # Reverse Geocoding (經緯度 -> Place ID)
    geo_params = {"latlng": f"{lat},{lng}", "key": GOOGLE_API_KEY, "language": "zh-TW"}
    try:
        geo_resp = requests.get(GEOCODE_URL, params=geo_params, timeout=5).json()

        if not geo_resp.get("results"):
            return {"name": "未知地點"}

        base_info = geo_resp["results"][0]
        place_id = base_info.get("place_id")
        address = base_info.get("formatted_address")

        # Place Details (Place ID -> 詳細名稱/評分)
        detail_params = {
            "place_id": place_id,
            "key": GOOGLE_API_KEY,
            "language": "zh-TW",
            "fields": "name,rating,url",
        }
        detail_resp = requests.get(
            GOOGLE_DETAILS_URL, params=detail_params, timeout=5
        ).json()
        result = detail_resp.get("result", {})

        return {
            "name": result.get("name") or address,  # 如果沒有店名，就顯示地址
            "rating": result.get("rating") or 0.0,
            "address": address,
            "google_map_url": result.get("url"),
        }
    except Exception as e:
        print(f"[Backend] Google API Error: {e}")
        return {"name": "地圖點擊位置", "address": ""}


# -----------------------------------
#   天氣與地點評分工具 (NEW)
# -----------------------------------
def compute_weather_score(station_key: str) -> float:
    """
    輸入捷運站 key，使用既有函式 fetch_cwa_wx() + parse_weather_info()
    回傳 0~100 的天氣分數
    """
    city = STATION_LOCATION_MAP.get(station_key.lower(), "臺北市")
    cwa_data = fetch_cwa_wx(city)
    wx_text = parse_weather_info(cwa_data)  # 例如：多雲時晴，氣溫 18-23°C

    score = 100

    # ---- 主／副天氣扣分邏輯 ----
    if "雨" in wx_text:
        score -= 20
    if "雷" in wx_text:
        score -= 30
    if "陰" in wx_text:
        score -= 10
    if "多雲" in wx_text:
        score -= 5
    if "涼" in wx_text:
        score -= 5
    if "炎熱" in wx_text:
        score -= 5

    return max(0, min(100, score))


def compute_place_score(lat: float, lng: float) -> float:
    """
    使用 get_place_info() 的 Google 評分，回傳 0~100 分。
    """
    try:
        place = get_place_info(lat, lng)

        rating = place.get("rating", 0.0)  # Google rating 1~5
        if not rating:
            return 60.0  # 沒資料，給一個保守值

        return (rating / 5.0) * 100.0

    except Exception as e:
        print("[Backend] Compute place score error:", e)
        return 60.0
