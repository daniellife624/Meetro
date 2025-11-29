import os
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

# 建立 Router
router = APIRouter(prefix="/api", tags=["weather_station"])

# -----------------------------------
#         設定與常數
# -----------------------------------

CWA_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
CWA_API_KEY = "CWA-624BB740-DC7B-48E2-9002-B077B72CB174"

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

STATION_ATTRACTIONS = {
    "songshan": ["饒河街夜市", "松山慈祐宮", "彩虹橋"],
    "gongguan": ["國立臺灣大學", "水源市場", "寶藏巖"],
    "xindian": ["碧潭吊橋", "和美山步道", "新店老街"],
}

GOOGLE_API_KEY = "AIzaSyAtF8UQRBtvHLVok_s7h2ItjLs0gaOFrqs"
GOOGLE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


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

    print(f"[CWA] Fetching weather for {location_name}...")  # Debug Log

    for attempt in range(retries + 1):
        try:
            resp = requests.get(CWA_URL, params=params, timeout=timeout)

            # Debug Log: 印出狀態碼
            print(f"[CWA] Status Code: {resp.status_code}")

            if resp.status_code != 200:
                print(f"[CWA] Error Response: {resp.text}")  # 印出錯誤訊息
                return {}

            return resp.json()
        except requests.RequestException as e:
            print(f"[CWA] Network Error Attempt {attempt+1}: {e}")
            if attempt == retries:
                return {}
            time.sleep(0.5)
    return {}


def parse_weather_info(cwa_data: Dict) -> str:
    try:
        # 檢查資料結構是否正確
        if "records" not in cwa_data or "location" not in cwa_data["records"]:
            print("[CWA] Invalid data structure")
            return ""

        location = cwa_data["records"]["location"][0]
        weather_elements = location["weatherElement"]

        wx = ""
        min_t = ""
        max_t = ""

        for el in weather_elements:
            if el["elementName"] == "Wx":
                wx = el["time"][0]["parameter"]["parameterName"]
            elif el["elementName"] == "MinT":
                min_t = el["time"][0]["parameter"]["parameterName"]
            elif el["elementName"] == "MaxT":
                max_t = el["time"][0]["parameter"]["parameterName"]

        result = f"{wx}，氣溫 {min_t}-{max_t}°C"
        print(f"[CWA] Parsed Result: {result}")  # Debug Log
        return result

    except Exception as e:
        print(f"[CWA] Parse Error: {e}")
        return ""


# -----------------------------------
#   API Endpoints
# -----------------------------------


@router.get("/stations/{station_key}")
def get_station_info(station_key: str):

    print(f"[API] Get station info for: {station_key}")  # Debug Log

    city = STATION_LOCATION_MAP.get(station_key.lower(), "臺北市")

    cwa_data = fetch_cwa_wx(city)
    weather_str = parse_weather_info(cwa_data)

    if not weather_str:
        # 如果 API 失敗，給一個更明顯的提示，方便 debug
        weather_str = f"暫無資料 (查詢: {city})"

    attractions = STATION_ATTRACTIONS.get(station_key.lower(), ["周邊景點探索中..."])

    return {"key": station_key, "weather": weather_str, "attractions": attractions}


@router.get("/google/place-info")
def get_place_info(lat: float = Query(...), lng: float = Query(...)):
    geo_params = {"latlng": f"{lat},{lng}", "key": GOOGLE_API_KEY}
    try:
        geo_resp = requests.get(GEOCODE_URL, params=geo_params, timeout=5).json()

        if not geo_resp.get("results"):
            return {"name": "未知地點"}

        base_info = geo_resp["results"][0]
        place_id = base_info.get("place_id")
        address = base_info.get("formatted_address")

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
            "name": result.get("name") or "選定位置",
            "rating": result.get("rating") or 0.0,
            "address": address,
            "google_map_url": result.get("url"),
        }
    except Exception as e:
        print(f"Google API Error: {e}")
        return {"name": "地圖點擊位置", "address": ""}
