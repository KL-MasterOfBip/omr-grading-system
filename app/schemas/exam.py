from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None
    num_questions: int = 40
    num_choices: int = 4


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    num_questions: Optional[int] = None
    num_choices: Optional[int] = None


class ExamResponse(ExamBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
