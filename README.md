# Meetro 專案開發說明文件

本專案是一個基於 Docker 容器化技術開發的旅遊媒合平台，整合了 FastAPI 後端、Vue 3 前端以及 SQLite 資料庫。本系統的核心功能為「動態成功率權重配置 (BCMS)」，允許管理員即時調整演算參數，以反映不同維度對用戶配對成功率的影響。

## 1. 系統技術棧與架構規範

- **前端框架 (Frontend)**: Vue 3 (Composition API), Pinia, Vue Router, Axios.
- **後端框架 (Backend)**: FastAPI (Python 3.10+), SQLAlchemy ORM, Pydantic.
- **資料庫 (Database)**: SQLite (單一檔案持久化於 Docker Volume).
- **部署環境 (DevOps)**: Docker, Docker Compose.
- **外部服務整合**:
  - **中央氣象署 (CWA) API**: 獲取即時預報數據，用於天氣因素權重計算.
  - **Google Maps Platform**: 執行地圖逆向編碼（Reverse Geocoding）與地點評分抓取.

## 2. 資料庫實體關係 (Database Schema)

系統採用 SQLAlchemy 定義資料模型，確保數據一致性與關聯完整性.

### 2.1 核心資料表說明

| 資料表              | 說明           | 關鍵欄位與限制                                             |
| :------------------ | :------------- | :--------------------------------------------------------- |
| **Users**           | 用戶帳戶與權限 | `email` (Unique), `hashed_password`, `role` (admin/user)   |
| **Stations**        | 捷運站點資料   | `key` (Unique Index), `latitude`, `longitude`              |
| **Attractions**     | 站點周邊景點   | `name`, `station_id` (ForeignKey)                          |
| **Invites**         | 媒合邀約記錄   | `sender_id`, `station_id`, `status` (預設為 open)          |
| **Matches**         | 配對與評分紀錄 | `invite_id`, `sender_id`, `receiver_id`, `feedback_status` |
| **Emas**            | 站點互動繪馬   | `user_id`, `station_id`, `content` (Max: 50 chars)         |
| **SystemVariables** | BCMS 參數配置  | `name` (Unique), `weight` (0-100), `rule_desc`             |

### 2.2 關聯邏輯設計

- **Match 雙向關聯**: `Match` 模型透過 `sender_id` 與 `receiver_id` 兩個外鍵同時指向 `Users` 表，並在 `User` 模型中定義明確的 `relationship` 以解決雙向指標歧義.
- **狀態追蹤**: `feedback_status` 用於追蹤發送方與接受方是否完成評分（pending, sender_done, receiver_done, both_done）.

## 3. 核心 API 端點規範

### 3.1 認證與用戶管理

- `POST /api/users/register`: 處理用戶註冊與資料初始化.
- `POST /api/users/login`: 驗證身分並核發 JWT Access Token.

### 3.2 權重控制系統 (BCMS)

- `GET /api/bcms/config`: 讀取當前權重參數。
- `POST /api/bcms/config/save`: 持久化管理員設定之權重（僅限管理者權限）。

### 3.3 環境數據與地理資訊 (Weather & Maps)

- `GET /api/stations/{station_key}`: 整合 CWA API 獲取即時天氣與資料庫景點。
- `GET /api/google/place-info`: 傳入經緯度，透過 Google Maps API 獲取地點名稱、評分及詳細地址。

### 3.4 邀約與計算邏輯

- `GET /api/invites`: 取得特定站點之開放邀約。此 API 會調用計算服務，返回包含 `sender_success_rate` 欄位的數據模型.
- `POST /api/matches/{invite_id}/accept`: 建立配對記錄，並自動注入發送方 ID 確保數據完整.

## 4. 環境初始化與啟動流程 (重要)

本專案之靜態站點資料與初始權重參數需透過初始化腳本注入 SQLite 資料庫。部署時請嚴格遵守以下順序：

### 步驟 4.1：環境清理

移除既有容器並刪除資料庫持久化卷：

```bash
docker-compose down
docker volume rm meetro_meetro_data
```

### 步驟 4.2：初始化資料庫結構與種子數據

先行啟動後端容器，並執行預設資料注入：

```bash
docker-compose up -d backend
docker exec meetro_backend python backend/init_data.py

```

### 步驟 4.3：完整建置與啟動

```bash
docker compose build --no-cache
docker compose up

```

## 5. 成功率演算邏輯 (Success Rate Service)

系統成功率演算位於 `backend/services/success_rate_service.py`，其公式結合了資料庫歷史數據與外部 API 之標準化數值。

### 5.1 天氣評分 (Weather Scoring)

系統調用 `compute_weather_score` 對氣象局回傳之天氣現象進行權重扣分：

- **基礎分**: 100 分。
- **扣分邏輯**: 「雷」(-30)、「雨」(-20)、「陰」(-10)、「多雲/涼/熱」(-5)。

### 5.2 地點評分 (Place Scoring)

系統透過 `compute_place_score` 將 Google Maps 的 1.0-5.0 評分轉化為 0-100 分之百分位數。若無外部資料，則採保守值 60.0。

### 5.3 最終演算公式

**最終成功率 = (歷史滿意度 × W1) + (天氣影響分數 × W2) + (地點熱門度 × W3)**
_其中權重 W1, W2, W3 由 Admin 透過 BCMS 介面動態調整。_

---

**備註：前端開發環境運行於 localhost:8080，後端 API 服務端點為 localhost:8001。**

```

```
