import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from db import crud

logger = logging.getLogger("chatbot")
logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        error_message = None
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as e:
            error_message = str(e)
            raise
        finally:
            latency_ms = int((time.time() - start) * 1000)
            logger.info(
                f"{request.method} {request.url.path} Status={status_code} Latency={latency_ms}ms"
            )

            try:
                crud.save_request_log(
                    conversation_id=None,
                    endpoint=request.url.path,
                    status_code=status_code,
                    latency_ms=latency_ms,
                    error_message=error_message,
                )
            except Exception:
                pass