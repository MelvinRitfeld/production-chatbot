from fastapi import FastAPI
from sqlalchemy import text
from db.session import SessionLocal
from app.llm.llm_service import LLMService


app = FastAPI(title="Production Chatbot API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return {"db": "ok"}

@app.post("/chat-test")
def chat_test(payload: dict):
    user_message = payload.get("message", "")
    style = payload.get("style", "instruction")

    llm = LLMService()
    result = llm.generate(user_message, style=style)

    return {"reply": result.reply}

