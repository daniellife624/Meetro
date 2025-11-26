"""
整合版 FastAPI：
- 天氣 API（中央氣象署 CWA）
- 捷運綠線附近店家搜尋（Google Places）
- 前端點擊 Google Map → 後端用經緯度查地點資訊
"""

import os
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse


# -----------------------------------
#         建立唯一 FastAPI 實例
# -----------------------------------
app = FastAPI(title="Weather + Google Places API Service")



# -----------------------------------
#        天氣 API 設定
# -----------------------------------

CWA_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
CWA_API_KEY = "CWA-624BB740-DC7B-48E2-9002-B077B72CB174"

CITY_MAP = {
    "taipei": "臺北市",
    "new_taipei": "新北市",
    "keelung": "基隆市",
    "taoyuan": "桃園市",
    "hsinchu": "新竹市",
    "miaoli": "苗栗縣",
    "taichung": "臺中市",
    "changhua": "彰化縣",
    "nantou": "南投縣",
    "yunlin": "雲林縣",
    "chiayi": "嘉義市",
    "tainan": "臺南市",
    "kaohsiung": "高雄市",
    "pingtung": "屏東縣",
    "yilan": "宜蘭縣",
    "hualien": "花蓮縣",
    "taitung": "臺東縣"
}

BASE_SCORE = {"晴": 100, "多雲": 80, "陰": 60, "霧": 60, "雨": 40, "雪": 40}
ADJUST_SCORE = {"晴": 5, "多雲": -10, "陰": -15, "霧": -15, "雨": -20, "雪": -20}



# -----------------------------------
#        天氣功能函式
# -----------------------------------

def fetch_cwa_wx(location_name: str, retries: int = 2, timeout: int = 8) -> Dict:
    token = os.environ.get("CWA_API_KEY") or CWA_API_KEY

    params = {
        "Authorization": token,
        "format": "JSON",
        "locationName": location_name,
        "elementName": "Wx"
    }

    for attempt in range(retries + 1):
        try:
            resp = requests.get(CWA_URL, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(0.8)


def parse_wx_descriptions(data: Dict) -> List[str]:
    locations = data.get("records", {}).get("location", [])
    if not locations:
        return []
    wx_elem = next((e for e in locations[0]["weatherElement"] if e["elementName"] == "Wx"), None)
    if not wx_elem:
        return []
    return [t["parameter"]["parameterName"] for t in wx_elem["time"]]


def score_weather(description: str) -> Dict:
    text = description.strip()
    keywords = ["晴", "多雲", "陰", "霧", "雨", "雪"]

    found = [(kw, text.find(kw)) for kw in keywords if text.find(kw) != -1]
    if not found:
        return {"description": text, "main": None, "subs": [], "score": 0}

    found.sort(key=lambda x: x[1])
    main = found[0][0]
    score = BASE_SCORE.get(main, 0)

    subs = []
    seen = {main}
    for kw, _ in found[1:]:
        if kw not in seen:
            subs.append(kw)
            seen.add(kw)
            score += ADJUST_SCORE.get(kw, 0)

    score = max(0, min(100, score))
    return {"description": text, "main": main, "subs": subs, "score": score}


def get_weather_scores(location_name: str):
    raw = fetch_cwa_wx(location_name)
    descs = parse_wx_descriptions(raw)
    return [score_weather(d) for d in descs]

# -----------------------------------
#        天氣時段功能
# -----------------------------------
TIME_FMT = "%Y-%m-%d %H:%M:%S"

def parse_wx_slots(cwa_json: Dict) -> List[Dict]:
    records = cwa_json.get("records", {})
    locations = records.get("location", [])
    if not locations:
        return []

    wx_elem = None
    for elem in locations[0].get("weatherElement", []):
        if elem.get("elementName") == "Wx":
            wx_elem = elem
            break

    if not wx_elem:
        return []

    slots = []
    for t in wx_elem.get("time", []):
        try:
            start_dt = datetime.strptime(t.get("startTime"), TIME_FMT)
            end_dt = datetime.strptime(t.get("endTime"), TIME_FMT)
        except:
            continue

        desc = t.get("parameter", {}).get("parameterName", "").strip()
        slots.append({"start": start_dt, "end": end_dt, "description": desc})

    return slots


def pick_slot_for_event(slots: List[Dict], event_time: datetime) -> Optional[Dict]:
    for s in slots:
        if s["start"] <= event_time < s["end"]:
            return s
    return None


def get_event_weather_score(location_name: str, event_time: datetime) -> Optional[Dict]:
    raw = fetch_cwa_wx(location_name)
    slots = parse_wx_slots(raw)
    if not slots:
        return None
    slot = pick_slot_for_event(slots, event_time)
    if not slot:
        return None
    return score_weather(slot["description"])


# -----------------------------------
#        天氣活動分數 Endpoint
# -----------------------------------
@app.get("/weather/event-score")
def api_event_score(location: str = Query(...), event_time: str = Query(...)):
    loc = CITY_MAP.get(location.lower(), location)
    try:
        dt = datetime.strptime(event_time, TIME_FMT)
    except:
        return JSONResponse(
            status_code=400,
            content={"error": "event_time 格式需為 YYYY-MM-DD HH:MM:SS"}
        )

    result = get_event_weather_score(loc, dt)
    return {
        "location": loc,
        "event_time": event_time,
        "result": result
    }


# -----------------------------------
#        天氣 API Endpoint
# -----------------------------------

@app.get("/weather/scores")
def api_weather_scores(location: str = Query(...)):
    loc = CITY_MAP.get(location.lower(), location)
    return {"location": loc, "scores": get_weather_scores(loc)}



# -----------------------------------
#        Google Places API 設定
# -----------------------------------

API_KEY = "AIzaSyAtF8UQRBtvHLVok_s7h2ItjLs0gaOFrqs"

GOOGLE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"



# -----------------------------------
#   ★ 新增：用經緯度查 Google 評分 API
# -----------------------------------

@app.get("/place-info")
def get_place_info(lat: float = Query(...), lng: float = Query(...)):
    """前端點選 Google Map 後提供坐標，由後端查該地點 Google 評分 + 地址"""

    # Step 1：Reverse Geocoding
    geo_params = {"latlng": f"{lat},{lng}", "key": API_KEY}
    geo_resp = requests.get(GEOCODE_URL, params=geo_params).json()

    if not geo_resp.get("results"):
        return {"error": "找不到此經緯度的資訊"}

    base_info = geo_resp["results"][0]
    place_id = base_info.get("place_id")
    address = base_info.get("formatted_address")

    # Step 2：Place Details
    detail_params = {
        "place_id": place_id,
        "key": API_KEY,
        "language": "zh-TW",
        "fields": "name,rating,formatted_address,geometry"
    }
    detail_resp = requests.get(GOOGLE_DETAILS_URL, params=detail_params).json()

    result = detail_resp.get("result", {})

    return {
        "name": result.get("name"),
        "rating": result.get("rating"),
        "address": result.get("formatted_address") or address,
        "lat": result.get("geometry", {}).get("location", {}).get("lat"),
        "lng": result.get("geometry", {}).get("location", {}).get("lng"),
        "google_map_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    }


# -----------------------------------
#   保留：捷運綠線附近搜尋
# -----------------------------------

GREEN_LINE_STATIONS = {
    "songshan": (25.049554, 121.578002),
    "nanjingsanmin": (25.051809, 121.566062),
    "taipeiarena": (25.051490, 121.553007),
    "nanjingfuxing": (25.052300, 121.544000),
    "songjiangnanjing": (25.052194, 121.533765),
    "zhongshan": (25.052708, 121.520944),
    "beimen": (25.049327, 121.510215),
    "ximen": (25.042233, 121.508052),
    "xiaonanmen": (25.038568, 121.511921),
    "chiangkaishekmemorialhall": (25.032729, 121.518087),
    "guting": (25.026245, 121.522187),
    "taipowerbuilding": (25.019503, 121.527266),
    "gongguan": (25.014333, 121.534904),
    "wanlong": (25.001944, 121.534407),
    "jingmei": (24.992602, 121.540749),
    "dapinglin": (24.982802, 121.541160),
    "qizhang": (24.974834, 121.541695),
    "xiaobitan": (24.9731, 121.52999),
    "xindiandistrictoffice": (24.967936, 121.541273),
    "xindian": (24.957595, 121.537861)
}


def get_nearby_places(lat, lng, keyword="cafe", radius=1500):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "language": "zh-TW",
        "type": "establishment",
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()

    results = []
    for place in response.get("results", []):
        place_id = place.get("place_id")
        results.append({
            "name": place.get("name"),
            "rating": place.get("rating"),
            "address": place.get("vicinity"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "google_map_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        })
    return results


@app.get("/places")
def api_places(station: str = Query(...), keyword: str = "cafe"):
    if station not in GREEN_LINE_STATIONS:
        return JSONResponse(
            status_code=400,
            content={"error": f"站名錯誤，可用站名：{list(GREEN_LINE_STATIONS.keys())}"}
        )
    lat, lng = GREEN_LINE_STATIONS[station]
    places = get_nearby_places(lat, lng, keyword)
    return {"station": station, "keyword": keyword, "results": places}
