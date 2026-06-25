from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class QuestionBase(BaseModel):
    order: int
    correct_answer: str  # "A" | "B" | "C" | "D"
    score: int = 1


class QuestionCreate(QuestionBase):
    exam_code_id: int


class QuestionUpdate(BaseModel):
    correct_answer: Optional[str] = None
    score: Optional[int] = None


class QuestionResponse(QuestionBase):
    id: int
    exam_code_id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
