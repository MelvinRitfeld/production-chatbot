# CRUD function stubs for backend contract
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

def create_conversation() -> UUID:
	"""Create a new conversation and return its UUID."""
	return uuid4()

def save_message(conversation_id: UUID, role: str, content: str) -> UUID:
	"""Save a message to a conversation and return its UUID."""
	return uuid4()

def get_conversation(conversation_id: UUID) -> Dict[str, Any]:
	"""Get a conversation and its messages as a dict."""
	return {
		"conversation": {"id": str(conversation_id)},
		"messages": []
	}

def save_request_log(
	conversation_id: Optional[UUID],
	endpoint: str,
	status_code: int,
	latency_ms: int,
	error_message: Optional[str]
) -> None:
	"""Save a request log entry."""
	pass

def get_metrics() -> Dict[str, Any]:
	"""Return metrics for admin endpoint."""
	return {
		"total_conversations": 0,
		"avg_latency_ms": 0.0,
		"error_count": 0
	}

def save_feedback(
	conversation_id: UUID,
	message_id: Optional[UUID],
	rating: int,
	comment: Optional[str]
) -> None:
	"""Save feedback for a message/conversation."""
	pass
