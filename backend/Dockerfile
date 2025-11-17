# ------------------------------------
# Backend Python Service (Python 3.11)
# ------------------------------------
FROM python:3.11-slim

# 環境變數
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 設置工作目錄
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .