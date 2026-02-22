
from fastapi import APIRouter, status
from app.models.chat import ChatRequest, ChatResponse
from app.llm.llm_service import LLMService
# from db.crud import save_message, create_conversation  # Uncomment when implemented
import uuid
import time

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(payload: ChatRequest):
	start = time.perf_counter()

	# Placeholder: create or use conversation_id
	conversation_id = payload.conversation_id or str(uuid.uuid4())

	# Placeholder: Call LLM service
	llm = LLMService()
	result = llm.generate(payload.message)

	# Placeholder: Save message to DB (stub)
	# save_message(conversation_id, "user", payload.message)
	# save_message(conversation_id, "assistant", result.reply)

	latency_ms = int((time.perf_counter() - start) * 1000)

	return ChatResponse(
		reply=result.reply,
		conversation_id=conversation_id,
		latency_ms=latency_ms
	)
