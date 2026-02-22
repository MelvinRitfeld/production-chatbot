
from fastapi import APIRouter, status
from app.models.admin import MetricsResponse
# from db.crud import get_metrics  # Uncomment when implemented

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/metrics", response_model=MetricsResponse, status_code=status.HTTP_200_OK)
async def metrics_endpoint():
	# Placeholder: Call get_metrics from CRUD (stub)
	# metrics = get_metrics()
	metrics = {
		"total_conversations": 0,
		"avg_latency_ms": 0.0,
		"error_count": 0
	}
	return MetricsResponse(**metrics)
