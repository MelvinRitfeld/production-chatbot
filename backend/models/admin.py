from pydantic import BaseModel
from typing import Optional, List


class MetricsResponse(BaseModel):
    total_conversations: int
    total_messages: int
    avg_latency_ms: float
    error_count: int
    success_rate: float


class RecentRequestLog(BaseModel):
    id: str
    endpoint: str
    status_code: int
    latency_ms: int
    error_message: Optional[str] = None
    created_at: Optional[str] = None


class RecentLogsResponse(BaseModel):
    logs: List[RecentRequestLog]