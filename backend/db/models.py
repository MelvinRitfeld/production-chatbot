import uuid

from sqlalchemy import (
    Column,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey


from .session import Base


# =========================
# A) conversations
# =========================
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    feedback = relationship(
        "Feedback",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


# =========================
# B) messages
# =========================
class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(Text, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

    feedback = relationship("Feedback", back_populates="message")

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="chk_messages_role"),
    )


# =========================
# C) request_logs
# =========================
class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=True)


    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
    )

    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source = Column(String, nullable=True)          # "faq" or "stub"
    faq_match_id = Column(String, nullable=True)    # e.g. "buku_kosten"
    faq_score = Column(Integer, nullable=True)      # your overlap score
    user_input = Column(Text, nullable=True)        # the actual user question

# =========================
# D) feedback
# =========================
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    # rating can be: -1/1 OR 1–5 (we allow -1,1,2,3,4,5)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    conversation = relationship("Conversation", back_populates="feedback")
    message = relationship("Message", back_populates="feedback")

    __table_args__ = (
        CheckConstraint("rating IN (-1, 1, 2, 3, 4, 5)", name="chk_feedback_rating"),
    )
