import os
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

# 建立 Router
router = APIRouter(prefix="/api", tags=["weather_map"])

# -----------------------------------
#         設定與常數
# -----------------------------------

# 中央氣象署開放資料平臺之資料擷取API
CWA_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
CWA_API_KEY = "CWA-624BB740-DC7B-48E2-9002-B077B72CB174"

# Google Maps API
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

# 靜態景點資料 (目前尚未有資料庫，先暫存於此)
STATION_ATTRACTIONS = {
    "songshan": ["饒河街夜市", "松山慈祐宮", "彩虹橋"],
    "gongguan": ["國立臺灣大學", "水源市場", "寶藏巖"],
    "xindian": ["碧潭吊橋", "和美山步道", "新店老街"],
}

# -----------------------------------
#         工具函式
# -----------------------------------


def fetch_cwa_wx(location_name: str, retries: int = 1, timeout: int = 5) -> Dict:
    token = os.environ.get("CWA_API_KEY") or CWA_API_KEY
    params = {
        "Authorization": CWA_API_KEY,
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
            else:
                print(f"[Backend] CWA Error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[Backend] Connection Error: {e}")
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
def get_station_info(station_key: str):
    """首頁：取得站點天氣與景點"""

    # 1. 取得縣市
    city = STATION_LOCATION_MAP.get(station_key.lower(), "臺北市")

    # 2. 抓取天氣
    cwa_data = fetch_cwa_wx(city)
    weather_str = parse_weather_info(cwa_data)

    # 3. 取得景點
    attractions = STATION_ATTRACTIONS.get(station_key.lower(), ["周邊景點探索中..."])

    return {"key": station_key, "weather": weather_str, "attractions": attractions}


@router.get("/google/place-info")
def get_place_info(lat: float = Query(...), lng: float = Query(...)):
    """SenderView：點擊地圖取得地點資訊"""

    # 1. Reverse Geocoding (經緯度 -> Place ID)
    geo_params = {"latlng": f"{lat},{lng}", "key": GOOGLE_API_KEY, "language": "zh-TW"}
    try:
        geo_resp = requests.get(GEOCODE_URL, params=geo_params, timeout=5).json()

        if not geo_resp.get("results"):
            return {"name": "未知地點"}

        base_info = geo_resp["results"][0]
        place_id = base_info.get("place_id")
        address = base_info.get("formatted_address")

        # 2. Place Details (Place ID -> 詳細名稱/評分)
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
