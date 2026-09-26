"""Time Server API — небольшое FastAPI-приложение для проверки CI/CD пайплайна."""

from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="Time Server API",
    description="Возвращает текущее время сервера в UTC.",
    version="0.1.0",
)


@app.get("/", tags=["service"])
def home() -> dict:
    return {
        "message": "Добро пожаловать в Time Server API",
        "docs": "/docs",
        "endpoints": ["/time", "/datetime", "/date"],
    }


@app.get("/health", tags=["service"])
def health() -> dict:
    return {"status": "healthy"}


@app.get("/time", tags=["time"])
def get_time() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "time": now.strftime("%H:%M:%S"),
        "timezone": "UTC",
    }


@app.get("/datetime", tags=["time"])
def get_datetime() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "datetime": now.isoformat(),
        "timezone": "UTC",
    }


@app.get("/date", tags=["time"])
def get_date() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "date": now.strftime("%Y-%m-%d"),
        "weekday": now.strftime("%A"),
        "timezone": "UTC",
    }
