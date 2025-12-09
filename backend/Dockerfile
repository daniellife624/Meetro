FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app/backend/
ENV PYTHONPATH=/app:$PYTHONPATH