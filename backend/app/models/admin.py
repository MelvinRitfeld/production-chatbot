
from pydantic import BaseModel

class MetricsResponse(BaseModel):
	total_conversations: int
	avg_latency_ms: float
	error_count: int
