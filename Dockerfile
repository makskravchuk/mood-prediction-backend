FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade --default-timeout=1200 --retries=10 -r /app/requirements.txt

COPY . .

EXPOSE 8000

RUN python init_resources.py