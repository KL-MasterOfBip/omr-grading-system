from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import ExamCreate, ExamUpdate, ExamResponse

router = APIRouter()


@router.get("/", response_model=List[ExamResponse])
def list_exams(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    repo = ExamRepository(db)
    return repo.get_all(skip=skip, limit=limit)


@router.post("/", response_model=ExamResponse, status_code=201)
def create_exam(
    exam_in: ExamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = ExamRepository(db)
    return repo.create(**exam_in.model_dump(), created_by=current_user.id)


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    repo = ExamRepository(db)
    exam = repo.get_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.put("/{exam_id}", response_model=ExamResponse)
def update_exam(
    exam_id: int,
    exam_in: ExamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = ExamRepository(db)
    exam = repo.update(exam_id, **exam_in.model_dump(exclude_none=True))
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.delete("/{exam_id}", status_code=204)
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = ExamRepository(db)
    if not repo.delete(exam_id):
        raise HTTPException(status_code=404, detail="Exam not found")
