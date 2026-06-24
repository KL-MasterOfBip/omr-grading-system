from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExamCodeBase(BaseModel):
    code: str
    description: Optional[str] = None


class ExamCodeCreate(ExamCodeBase):
    exam_id: int


class ExamCodeUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


class ExamCodeResponse(ExamCodeBase):
    id: int
    exam_id: int
    created_at: datetime

    class Config:
        from_attributes = True
