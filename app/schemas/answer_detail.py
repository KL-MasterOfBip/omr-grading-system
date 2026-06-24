from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnswerDetailBase(BaseModel):
    scan_result_id: int
    question_id: int
    selected_answer: Optional[str] = None
    is_correct: bool = False


class AnswerDetailCreate(AnswerDetailBase):
    pass


class AnswerDetailResponse(AnswerDetailBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
