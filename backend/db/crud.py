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
) -> None:
    db: Session = SessionLocal()
    try:
        log = RequestLog(
            conversation_id=conversation_id,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
            error_message=error_message,
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_metrics() -> Dict[str, Any]:
    """
    Returns:
    {
      "total_conversations": int,
      "avg_latency_ms": float,
      "error_count": int
    }
    """
    db: Session = SessionLocal()
    try:
        total_conversations = db.scalar(select(func.count(Conversation.id))) or 0

        avg_latency = db.scalar(select(func.avg(RequestLog.latency_ms)))
        avg_latency_ms = float(avg_latency) if avg_latency is not None else 0.0

        error_count = (
            db.scalar(select(func.count(RequestLog.id)).where(RequestLog.status_code >= 400))
            or 0
        )

        return {
            "total_conversations": int(total_conversations),
            "avg_latency_ms": avg_latency_ms,
            "error_count": int(error_count),
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