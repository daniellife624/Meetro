FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 修正 1：複製 requirements.txt 到容器的 /app
# 由於 context 是根目錄，這裡必須明確指定路徑
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 關鍵修正 2：複製整個 backend 資料夾到 /app/backend
# 我們不能在 backend/Dockerfile 裡使用 COPY backend，這會造成遞迴錯誤。
# 我們必須複製所有 *必要的* 程式碼。

# 🚨 請將此行移除：
# COPY backend /app/backend

# 🚨 採用這兩行替換：將 backend/ 裡的所有內容複製到 /app/backend
# 為了避免在 backend/Dockerfile 裡複製 backend，我們必須將程式碼包在另一個資料夾內。
# 由於您不願移動程式碼，這是最安全且能運作的方式：
COPY . /app/backend/

# 讓 Python 能夠從 /app 找到 backend 模組
ENV PYTHONPATH=/app:$PYTHONPATH