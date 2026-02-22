from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_middleware import LoggingMiddleware
from app.routers import chat, admin, health

app = FastAPI(title="Production Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(admin.router)
