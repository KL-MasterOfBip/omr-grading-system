from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.exam_code import ExamCode
from app.schemas.exam_code import ExamCodeCreate, ExamCodeUpdate, ExamCodeResponse

router = APIRouter()


@router.get("/exam/{exam_id}", response_model=List[ExamCodeResponse])
def list_exam_codes(exam_id: int, db: Session = Depends(get_db)):
    return db.query(ExamCode).filter(ExamCode.exam_id == exam_id).all()


@router.post("/", response_model=ExamCodeResponse, status_code=201)
def create_exam_code(
    exam_code_in: ExamCodeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    obj = ExamCode(**exam_code_in.model_dump(), created_by=current_user.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{exam_code_id}", status_code=204)
def delete_exam_code(
    exam_code_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    obj = db.query(ExamCode).filter(ExamCode.id == exam_code_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="ExamCode not found")
    db.delete(obj)
    db.commit()