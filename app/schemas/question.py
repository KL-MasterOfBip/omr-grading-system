from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class QuestionBase(BaseModel):
    order: int
    correct_answer: str  # "A" | "B" | "C" | "D"
    score: int = 1


class QuestionCreate(QuestionBase):
    exam_id: int


class QuestionUpdate(BaseModel):
    correct_answer: Optional[str] = None
    score: Optional[int] = None


class QuestionResponse(QuestionBase):
    id: int
    exam_id: int
    created_at: datetime

    class Config:
        from_attributes = True
