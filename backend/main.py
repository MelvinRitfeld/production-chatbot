from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_middleware import LoggingMiddleware
from routers.health import router as health_router
from routers.chat import router as chat_router
from routers.admin import router as admin_router
from db.session import init_db
from routers.feedback import router as feedback_router
from app.security.rate_limiter import rate_limit_middleware


app = FastAPI(title="Production Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "https://renewed-recreation-production-a5fa.up.railway.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
async def startup():
    init_db()

# health_router likely defines its own paths like "/health"
app.include_router(health_router)

# chat_router likely has no prefix, so we add "/api" here
app.include_router(chat_router, prefix="/api", tags=["chat"])

# admin_router ALREADY has prefix="/api/admin" inside routers/admin.py
# so DO NOT add prefix again here
app.include_router(admin_router)

# Add rate limiting middleware to the app
app.middleware("http")(rate_limit_middleware)


app.include_router(feedback_router, prefix="/api", tags=["feedback"])
