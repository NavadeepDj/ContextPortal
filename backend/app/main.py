from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import HttpUrl

from app.config import settings
from app.core.retriever import (
    AccessDeniedError,
    AuthenticationRequiredError,
    FetchError,
    get_context,
)
from app.redis import check_redis_connection

app = FastAPI(title=settings.app_name)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    if request.scope.get("endpoint") is fetch_context:
        detail = [
            {
                "loc": error["loc"],
                "msg": "A valid HTTP(S) URL is required.",
                "type": error["type"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(status_code=422, content={"detail": detail})
    return await request_validation_exception_handler(request, exc)


@app.get("/health")
async def health_check() -> dict[str, str]:
    redis_connected = await check_redis_connection()
    return {"status": "ok", "redis": "connected" if redis_connected else "disconnected"}


@app.get("/c", response_class=PlainTextResponse)
async def fetch_context(url: HttpUrl) -> str:
    """
    MVP Endpoint: Agent requests a URL.
    ContextPortal retrieves it (publicly or via authorized browser session)
    and returns clean Markdown.
    """
    try:
        result = await get_context(str(url))
    except AuthenticationRequiredError as exc:
        raise HTTPException(
            status_code=401, detail={"code": exc.code, "message": str(exc)}
        ) from None
    except AccessDeniedError as exc:
        raise HTTPException(
            status_code=403, detail={"code": exc.code, "message": str(exc)}
        ) from None
    except Exception:
        error = FetchError()
        raise HTTPException(
            status_code=500, detail={"code": error.code, "message": str(error)}
        ) from None
    return result.content
