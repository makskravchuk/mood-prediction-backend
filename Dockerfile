FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fonts-freefont-ttf \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade --default-timeout=1200 --retries=10 -r /app/requirements.txt

COPY . .

COPY mood_prediction/machine_learning/goemotions_model /app/mood_prediction/machine_learning/goemotions_model

EXPOSE 8000

RUN python init_resources.py