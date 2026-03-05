from fastapi import APIRouter
from db import crud
from models.admin import MetricsResponse, RecentLogsResponse
from db.crud import get_unmatched_questions

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/metrics", response_model=MetricsResponse)
def metrics():
    data = crud.get_metrics()
    return MetricsResponse(**data)

@router.get("/recent", response_model=RecentLogsResponse)
def recent():
    logs = crud.get_recent_request_logs(limit=20)
    return {"logs": logs}

@router.get("/unmatched")
def unmatched(limit: int = 20):
    return get_unmatched_questions(limit=limit)