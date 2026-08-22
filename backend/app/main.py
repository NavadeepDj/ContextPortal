from fastapi import FastAPI
from app.config import settings
from app.redis import check_redis_connection

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health_check():
    redis_connected = await check_redis_connection()
    return {
        "status": "ok",
        "redis": "connected" if redis_connected else "disconnected"
    }
