from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from db import crud

router = APIRouter()


class FeedbackRequest(BaseModel):
    conversation_id: UUID
    message_id: Optional[UUID] = None
    rating: int  # 1 = thumbs up, -1 = thumbs down
    comment: Optional[str] = None


@router.post("/feedback")
def submit_feedback(payload: FeedbackRequest):
    crud.save_feedback(
        conversation_id=payload.conversation_id,
        message_id=payload.message_id,
        rating=payload.rating,
        comment=payload.comment,
    )
    return {"status": "ok"}