from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse

router = APIRouter()


@router.get("/exam/{exam_id}", response_model=List[QuestionResponse])
def get_questions_by_exam(exam_id: int, db: Session = Depends(get_db)):
    repo = QuestionRepository(db)
    return repo.get_by_exam(exam_id)


@router.post("/", response_model=QuestionResponse, status_code=201)
def create_question(
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = QuestionRepository(db)
    return repo.create(**question_in.model_dump())


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = QuestionRepository(db)
    q = repo.update(question_id, **question_in.model_dump(exclude_none=True))
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = QuestionRepository(db)
    if not repo.delete(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
