from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse

router = APIRouter()


@router.get("/exam-code/{exam_code_id}", response_model=List[QuestionResponse])
def get_questions_by_exam_code(exam_code_id: int, db: Session = Depends(get_db)):
    repo = QuestionRepository(db)
    return repo.get_by_exam_code(exam_code_id)


@router.post("/", response_model=QuestionResponse, status_code=201)
def create_question(
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = QuestionRepository(db)
    question_data = question_in.model_dump()
    question_data["created_by"] = current_user.id
    return repo.create(**question_data)


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


@router.put("/bulk/{exam_code_id}", response_model=dict)
def bulk_upsert_questions(
    exam_code_id: int,
    questions_in: List[QuestionBase],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Cập nhật hoặc tạo mới danh sách đáp án cho một mã đề.
    Duyệt qua từng câu, nếu đã có (theo exam_code_id và order) thì update, nếu chưa có thì create.
    """
    repo = QuestionRepository(db)
    existing_questions = repo.get_by_exam_code(exam_code_id)
    # Tạo map {order: question_obj}
    existing_map = {q.order: q for q in existing_questions}
    
    updated_count = 0
    created_count = 0
    
    for q_in in questions_in:
        if q_in.order in existing_map:
            # Cập nhật
            repo.update(existing_map[q_in.order].id, correct_answer=q_in.correct_answer, score=q_in.score)
            updated_count += 1
        else:
            # Tạo mới
            repo.create(
                exam_code_id=exam_code_id,
                order=q_in.order,
                correct_answer=q_in.correct_answer,
                score=q_in.score,
                created_by=current_user.id
            )
            created_count += 1
            
    return {"message": "Success", "updated": updated_count, "created": created_count}


@router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = QuestionRepository(db)
    if not repo.delete(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
