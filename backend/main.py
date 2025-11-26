from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="Taipei MRT Green Line Places API")

API_KEY = "AIzaSyAtF8UQRBtvHLVok_s7h2ItjLs0gaOFrqs"

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
        "radius": radius,    # 半徑 1500m
        "keyword": keyword,  # 用關鍵字搜尋
        "language": "zh-TW",
        "type": "establishment",  # 最廣泛的商家類型
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()
    print("Google API Response Status:", response.get("status"))

    results = []
    for place in response.get("results", []):
        name = place.get("name")
        rating = place.get("rating")
        address = place.get("vicinity")
        place_id = place.get("place_id")
        google_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

        results.append({
            "name": name,
            "rating": rating,
            "address": address,
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "google_map_url": google_url
        })

    return results



@app.get("/places")
def get_places(
    station: str = Query(...),
    keyword: str = Query("cafe")
):
    if station not in GREEN_LINE_STATIONS:
        return JSONResponse(
            status_code=400,
            content={"error": f"站名錯誤，可用站名：{list(GREEN_LINE_STATIONS.keys())}"}
        )

    lat, lng = GREEN_LINE_STATIONS[station]
    places = get_nearby_places(lat, lng, keyword)

    return {
        "station": station,
        "keyword": keyword,
        "total_results": len(places),
        "results": places
    }
