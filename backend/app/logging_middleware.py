import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.db.crud import save_request_log


logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        conversation_id = None
        status_code = 500
        error_message = None

        try:
            response: Response = await call_next(request)
            status_code = response.status_code
            return response

        except Exception as exc:
            error_message = str(exc)
            raise exc

        finally:
            latency_ms = int((time.perf_counter() - start_time) * 1000)

            logger.info(
                f"{request.method} {request.url.path} "
                f"status={status_code} latency_ms={latency_ms}"
            )

            try:
                save_request_log(
                    conversation_id=conversation_id,
                    endpoint=request.url.path,
                    status_code=status_code,
                    latency_ms=latency_ms,
                    error_message=error_message,
                )
            except Exception:
                # We never want logging failure to break the API
                pass
