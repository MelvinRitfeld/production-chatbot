import time
from fastapi import APIRouter

from models.chat import ChatRequest, ChatResponse
from app.services.faq_service import FAQService
from db import crud

router = APIRouter()
faq = FAQService()

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    start = time.time()

    conversation_id = payload.conversation_id
    if conversation_id is None:
        conversation_id = crud.create_conversation()

    # Save user message
    crud.save_message(
        conversation_id=conversation_id,
        role="user",
        content=payload.message,
    )

    # Get answer (FAQ first, then LLM fallback)
    reply_text, source = faq.get_answer(payload.message)

    # Save assistant message
    crud.save_message(
        conversation_id=conversation_id,
        role="assistant",
        content=reply_text,
    )

    latency_ms = int((time.time() - start) * 1000)

    return ChatResponse(
        reply=reply_text,
        conversation_id=conversation_id,
        latency_ms=latency_ms,
    )