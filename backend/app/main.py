from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import HttpUrl

from app.config import settings
from app.redis import check_redis_connection
from app.core.retriever import get_context

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health_check():
    redis_connected = await check_redis_connection()
    return {
        "status": "ok",
        "redis": "connected" if redis_connected else "disconnected"
    }

@app.get("/c", response_class=PlainTextResponse)
async def fetch_context(url: HttpUrl):
    """
    MVP Endpoint: Agent requests a URL. 
    ContextPortal retrieves it (publicly or via authorized browser session)
    and returns clean Markdown.
    """
    try:
        markdown_content = await get_context(str(url))
        return markdown_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
