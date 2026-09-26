"""Time Server API — небольшое FastAPI-приложение для проверки CI/CD пайплайна."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Time Server API",
    description="Возвращает текущее время сервера и конвертирует его по часовым поясам.",
    version="1.0.0",
)


@app.get("/", tags=["service"])
def home() -> dict:
    return {
        "message": "Добро пожаловать в Time Server API",
        "docs": "/docs",
        "endpoints": ["/time", "/datetime", "/date", "/convert"],
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


@app.get("/convert", tags=["time"])
def convert(
    time: str = Query(..., description="Время в формате HH:MM, например 14:30"),
    city: str = Query(..., description="Часовой пояс, например Europe/Moscow"),
) -> dict:
    try:
        parsed = datetime.strptime(time, "%H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат времени. Ожидается HH:MM")

    try:
        source_tz = ZoneInfo(city)
    except (ZoneInfoNotFoundError, ValueError):
        raise HTTPException(status_code=400, detail=f"Неизвестный часовой пояс: {city}")

    today = datetime.now(timezone.utc).astimezone(source_tz).date()
    localized = datetime.combine(today, parsed.time(), tzinfo=source_tz)
    return {
        "source": {"time": parsed.strftime("%H:%M"), "city": city},
        "target": {
            "time": localized.astimezone(timezone.utc).strftime("%H:%M"),
            "city": "UTC",
        },
    }
