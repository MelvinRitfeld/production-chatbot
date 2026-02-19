from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func

from .session import SessionLocal
from .models import Conversation, Message, RequestLog, Feedback

def get_db() -> Session:
    return SessionLocal()

def create_conversation() -> UUID:
    db = get_db()
    try:
        conversation = Conversation()
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def save_message(conversation_id: UUID, role: str, content: str) -> UUID:
    db = get_db()
    try:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message.id
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_conversation(conversation_id: UUID) -> dict:
    db = get_db()
    try:
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if not conversation:
            return {"conversation": None, "messages": []}

        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .all()
        )

        return {
            "conversation": {
                "id": conversation.id,
                "created_at": conversation.created_at,
            },
            "messages": [
                {
                    "id": m.id,
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
    conversation_id: UUID | None,
    endpoint: str,
    status_code: int,
    latency_ms: int,
    error_message: str | None,
):
    db = get_db()
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

def get_metrics() -> dict:
    db = get_db()
    try:
        total_conversations = db.query(func.count(Conversation.id)).scalar() or 0
        avg_latency = db.query(func.avg(RequestLog.latency_ms)).scalar() or 0
        error_count = (
            db.query(func.count(RequestLog.id))
            .filter(RequestLog.status_code >= 400)
            .scalar()
            or 0
        )

        return {
            "total_conversations": total_conversations,
            "avg_latency_ms": float(avg_latency),
            "error_count": error_count,
        }
    finally:
        db.close()

def save_feedback(
    conversation_id: UUID,
    message_id: UUID | None,
    rating: int,
    comment: str | None,
):
    db = get_db()
    try:
        feedback = Feedback(
            conversation_id=conversation_id,
            message_id=message_id,
            rating=rating,
            comment=comment,
        )
        db.add(feedback)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally: