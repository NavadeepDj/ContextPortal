import redis.asyncio as redis
from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

async def check_redis_connection() -> bool:
    try:
        await redis_client.ping()
        return True
    except redis.ConnectionError:
        return False
