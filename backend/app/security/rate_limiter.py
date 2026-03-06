import time
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# ── Configuration ─────────────────────────────────────────────────────────────
RATE_LIMIT_REQUESTS = 20       # max requests per window
RATE_LIMIT_WINDOW_SECONDS = 60  # per 60 seconds
BLOCK_DURATION_SECONDS = 120    # block for 2 minutes after exceeding limit

# ── In-memory store ───────────────────────────────────────────────────────────
# Format: { ip: { "requests": [timestamps], "blocked_until": float } }
_request_store: dict = defaultdict(lambda: {"requests": [], "blocked_until": 0.0})


def _get_client_ip(request: Request) -> str:
    """Extract real client IP, respecting reverse proxy headers."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware.
    Limits each IP to RATE_LIMIT_REQUESTS per RATE_LIMIT_WINDOW_SECONDS.
    Only applies to the /chat endpoint.
    """
    # Only rate limit the chat endpoint
    if request.url.path != "/api/chat":
        return await call_next(request)

    ip = _get_client_ip(request)
    now = time.time()
    record = _request_store[ip]

    # Check if currently blocked
    if record["blocked_until"] > now:
        retry_after = int(record["blocked_until"] - now)
        return JSONResponse(
            status_code=429,
            content={
                "detail": (
                    "Je stuurt te veel berichten. "
                    f"Probeer het opnieuw over {retry_after} seconden."
                )
            },
            headers={"Retry-After": str(retry_after)},
        )

    # Clean up old timestamps outside the window
    record["requests"] = [
        t for t in record["requests"]
        if now - t < RATE_LIMIT_WINDOW_SECONDS
    ]

    # Check rate limit
    if len(record["requests"]) >= RATE_LIMIT_REQUESTS:
        record["blocked_until"] = now + BLOCK_DURATION_SECONDS
        return JSONResponse(
            status_code=429,
            content={
                "detail": (
                    "Te veel berichten in korte tijd. "
                    f"Wacht {BLOCK_DURATION_SECONDS} seconden en probeer opnieuw."
                )
            },
            headers={"Retry-After": str(BLOCK_DURATION_SECONDS)},
        )

    # Record this request
    record["requests"].append(now)

    return await call_next(request)