# backend/place_routes.py
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests

# 建立 Router
router = APIRouter(prefix="/api/places", tags=["places"])

API_KEY = "AIzaSyAtF8UQRBtvHLVok_s7h2ItjLs0gaOFrqs"

# 捷運綠線座標表
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
    "xindian": (24.957595, 121.537861),
}


def get_nearby_places(lat, lng, keyword="cafe", radius=1500):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "language": "zh-TW",
        "type": "establishment",
        "key": API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        results = []
        # 限制回傳數量，避免資料過多
        for place in data.get("results", [])[:15]:
            place_id = place.get("place_id")

            # 安全取得經緯度
            location = place.get("geometry", {}).get("location", {})

            results.append(
                {
                    "name": place.get("name"),
                    "rating": place.get("rating", 0),
                    "user_ratings_total": place.get("user_ratings_total", 0),
                    "address": place.get("vicinity"),
                    "lat": location.get("lat"),
                    "lng": location.get("lng"),
                    "google_map_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                }
            )
        return results
    except Exception as e:
        print(f"[Backend] Place API Error: {e}")
        return []


@router.get("")  # 對應路徑: /api/places
def get_places(station: str = Query(...), keyword: str = Query("cafe")):
    station_key = station.lower()

    if station_key not in GREEN_LINE_STATIONS:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"站名錯誤，可用站名：{list(GREEN_LINE_STATIONS.keys())}"
            },
        )

    lat, lng = GREEN_LINE_STATIONS[station_key]
    places = get_nearby_places(lat, lng, keyword)

    return {
        "station": station_key,
        "keyword": keyword,
        "total_results": len(places),
        "results": places,
    }
