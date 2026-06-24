from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ScanResultBase(BaseModel):
    exam_id: int
    exam_code_id: Optional[int] = None
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    image_path: Optional[str] = None
    total_score: float = 0.0
    max_score: float = 0.0
    notes: Optional[str] = None


class ScanResultCreate(ScanResultBase):
    pass


class ScanResultUpdate(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    total_score: Optional[float] = None
    notes: Optional[str] = None


class ScanResultResponse(ScanResultBase):
    id: int
    scanned_at: datetime

    class Config:
        from_attributes = True
