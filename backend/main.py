from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text

from db.session import SessionLocal, init_db
from app.llm.llm_service import LLMService
from app.security.injection import check_prompt_injection
from app.security.fallbacks import safe_fallback_response


app = FastAPI(title="Production Chatbot API")

llm = LLMService()


class ChatTestIn(BaseModel):
    message: str
    style: str = "instruction"


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return {"db": "ok"}


@app.post("/chat-test")
def chat_test(payload: ChatTestIn):
    user_message = (payload.message or "").strip()
    style = payload.style or "instruction"

    check = check_prompt_injection(user_message)

    if check.is_suspicious:
        return {
            "reply": safe_fallback_response(),
            "blocked": True,
            "score": check.score,
            "reasons": check.reasons,
        }

    result = llm.generate(user_message, style=style)

    return {
        "reply": result.reply,
        "blocked": False,
        "score": check.score,
        "reasons": check.reasons,
    }