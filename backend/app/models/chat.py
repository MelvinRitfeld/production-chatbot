
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ChatRequest(BaseModel):
	message: str
	conversation_id: Optional[UUID] = None

class ChatResponse(BaseModel):
	reply: str
	conversation_id: UUID
	latency_ms: int
