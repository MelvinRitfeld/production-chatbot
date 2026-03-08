from __future__ import annotations

import uuid
from typing import Optional, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .session import SessionLocal
from .models import Conversation, Message, RequestLog, Feedback


def create_conversation() -> uuid.UUID:
    db: Session = SessionLocal()
    try:
        convo = Conversation()
        db.add(convo)
        db.commit()
        db.refresh(convo)
        return convo.id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def save_message(conversation_id: uuid.UUID, role: str, content: str) -> uuid.UUID:
    db: Session = SessionLocal()
    try:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg.id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_conversation(conversation_id: uuid.UUID) -> Dict[str, Any]:
    """
    Returns:
    {
        "conversation": {...} | None,
        "messages": [...]
    }
    """
    db: Session = SessionLocal()
    try:
        convo = db.get(Conversation, conversation_id)
        if convo is None:
            return {"conversation": None, "messages": []}

        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        messages = db.execute(stmt).scalars().all()

        return {
            "conversation": {
                "id": convo.id,
                "created_at": convo.created_at,
            },
            "messages": [
                {
                    "id": m.id,
                    "conversation_id": m.conversation_id,
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at,
                }
                for m in messages
            ],
        }
    finally:
        db.close()


def save_request_log(
    conversation_id: Optional[uuid.UUID],
    endpoint: str,
    status_code: int,
    latency_ms: int,
    error_message: Optional[str],
    source: Optional[str] = None,          # ✅ NEW
    faq_match_id: Optional[str] = None,    # ✅ NEW
    faq_score: Optional[int] = None,       # ✅ NEW
    user_input: Optional[str] = None,      # ✅ NEW
) -> None:
    db: Session = SessionLocal()
    try:
        log = RequestLog(
            conversation_id=conversation_id,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message,
            source=source,
            faq_match_id=faq_match_id,
            faq_score=faq_score,
            user_input=user_input,
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_metrics() -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        total_conversations = db.scalar(select(func.count(Conversation.id))) or 0
        total_messages = db.scalar(select(func.count(Message.id))) or 0

        avg_latency = db.scalar(select(func.avg(RequestLog.latency_ms)))
        avg_latency_ms = float(avg_latency) if avg_latency is not None else 0.0

        error_count = (
            db.scalar(select(func.count(RequestLog.id)).where(RequestLog.status_code >= 400))
            or 0
        )

        # ✅ only chat requests count for match rate
        total_chat_requests = (
            db.scalar(select(func.count(RequestLog.id)).where(RequestLog.endpoint == "/api/chat"))
            or 0
        )

        faq_matches = (
            db.scalar(
                select(func.count(RequestLog.id)).where(
                    (RequestLog.endpoint == "/api/chat") & (RequestLog.source == "faq")
                )
            )
            or 0
        )

        unmatched = (
            db.scalar(
                select(func.count(RequestLog.id)).where(
                    (RequestLog.endpoint == "/api/chat") & (RequestLog.source == "stub")
                )
            )
            or 0
        )

        match_rate = (faq_matches / total_chat_requests) if total_chat_requests > 0 else 0.0

        success_rate = 1.0 - (
            error_count / (db.scalar(select(func.count(RequestLog.id))) or 1)
        )

        return {
            "total_conversations": int(total_conversations),
            "total_messages": int(total_messages),
            "avg_latency_ms": avg_latency_ms,
            "error_count": int(error_count),
            "success_rate": float(success_rate),
            # ✅ NEW
            "total_chat_requests": int(total_chat_requests),
            "faq_matches": int(faq_matches),
            "unmatched": int(unmatched),
            "match_rate": float(match_rate),
        }
    finally:
        db.close()



def get_unmatched_questions(limit: int = 20) -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        stmt = (
            select(RequestLog)
            .where(
                (RequestLog.endpoint == "/api/chat") &
                (RequestLog.source == "stub")
            )
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )

        rows = db.execute(stmt).scalars().all()

        return {
            "count": len(rows),
            "items": [
                {
                    "id": str(r.id),
                    "created_at": r.created_at,
                    "user_input": r.user_input,
                    "status_code": r.status_code,
                }
                for r in rows
            ],
        }
    finally:
        db.close()
        

def save_feedback(
    conversation_id: uuid.UUID,
    message_id: Optional[uuid.UUID],
    rating: int,
    comment: Optional[str],
) -> None:
    db: Session = SessionLocal()
    try:
        fb = Feedback(
            conversation_id=conversation_id,
            message_id=message_id,
            rating=rating,
            comment=comment,
        )
        db.add(fb)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

        


def get_recent_request_logs(limit: int = 20):
    db: Session = SessionLocal()
    try:
        stmt = (
            select(RequestLog)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )
        logs = db.execute(stmt).scalars().all()

        return [
            {
                "id": str(l.id),
                "endpoint": l.endpoint,
                "status_code": l.status_code,
                "latency_ms": l.latency_ms,
                "error_message": l.error_message,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in logs
        ]
    finally:
        db.close()

def get_messages(conversation_id: uuid.UUID, limit: int = 6) -> list:
    """Returns the last N messages for a conversation, ordered oldest first."""
    db: Session = SessionLocal()
    try:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = db.execute(stmt).scalars().all()
        return [
            {"role": m.role, "content": m.content}
            for m in reversed(messages)
        ]
    finally:
        db.close()