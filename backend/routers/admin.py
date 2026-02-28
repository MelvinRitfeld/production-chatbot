from fastapi import APIRouter
from models.admin import MetricsResponse
from db import crud

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
def metrics():
    data = crud.get_metrics()
    return MetricsResponse(**data)