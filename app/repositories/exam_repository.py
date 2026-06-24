from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.exam import Exam


class ExamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, exam_id: int) -> Optional[Exam]:
        return self.db.query(Exam).filter(Exam.id == exam_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Exam]:
        return self.db.query(Exam).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> Exam:
        exam = Exam(**kwargs)
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def update(self, exam_id: int, **kwargs) -> Optional[Exam]:
        exam = self.get_by_id(exam_id)
        if not exam:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(exam, key, value)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def delete(self, exam_id: int) -> bool:
        exam = self.get_by_id(exam_id)
        if not exam:
            return False
        self.db.delete(exam)
        self.db.commit()
        return True
