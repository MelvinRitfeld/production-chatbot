from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_middleware import LoggingMiddleware
from routers.health import router as health_router
from routers.chat import router as chat_router
from routers.admin import router as admin_router

app = FastAPI(title="Production Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(health_router)
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])