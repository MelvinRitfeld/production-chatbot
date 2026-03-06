import time
from fastapi import APIRouter

from models.chat import ChatRequest, ChatResponse
from app.services.faq_service import FAQService
from app.security.injection import check_prompt_injection, check_pii
from app.security.fallbacks import (
    safe_fallback_response,
    empty_input_response,
    api_error_response,
)
from db import crud

router = APIRouter()
faq = FAQService()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    start = time.time()

    # ── 1. Empty input check ─────────────────────────────────────────────────
    if not payload.message or not payload.message.strip():
        return ChatResponse(
            reply=empty_input_response(),
            conversation_id=payload.conversation_id or crud.create_conversation(),
            latency_ms=0,
        )

    # ── 2. Prompt injection check ────────────────────────────────────────────
    injection_result = check_prompt_injection(payload.message)
    if injection_result.is_suspicious:
        conversation_id = payload.conversation_id or crud.create_conversation()
        crud.save_message(
            conversation_id=conversation_id,
            role="user",
            content=f"[BLOCKED: {', '.join(injection_result.reasons)}] {payload.message}",
        )
        return ChatResponse(
            reply=safe_fallback_response(),
            conversation_id=conversation_id,
            latency_ms=int((time.time() - start) * 1000),
        )

    # ── 3. PII check (log but don't block) ───────────────────────────────────
    pii_detected = check_pii(payload.message)

    # ── 4. Conversation setup ────────────────────────────────────────────────
    conversation_id = payload.conversation_id
    if conversation_id is None:
        conversation_id = crud.create_conversation()

    # ── 5. Save user message (anonymized if PII detected) ────────────────────
    safe_content = "[PII_REDACTED]" if pii_detected else payload.message
    crud.save_message(
        conversation_id=conversation_id,
        role="user",
        content=safe_content,
    )

    # ── 6. Get answer (FAQ first, then LLM fallback) ─────────────────────────
    try:
        reply_text, source = faq.get_answer(payload.message)
    except Exception:
        reply_text = api_error_response()
        source = "error"

    # ── 7. Save assistant message ────────────────────────────────────────────
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