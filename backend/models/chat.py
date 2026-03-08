from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: UUID
    latency_ms: int
    source: str = "llm"  # "faq", "llm", or "error"
    suggestions: List[str] = []  # Related FAQ questions shown when source is "llm"