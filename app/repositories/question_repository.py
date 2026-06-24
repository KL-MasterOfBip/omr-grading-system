from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.question import Question


class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, question_id: int) -> Optional[Question]:
        return self.db.query(Question).filter(Question.id == question_id).first()

    def get_by_exam(self, exam_id: int) -> List[Question]:
        return (
            self.db.query(Question)
            .filter(Question.exam_id == exam_id)
            .order_by(Question.order)
            .all()
        )

    def create(self, **kwargs) -> Question:
        q = Question(**kwargs)
        self.db.add(q)
        self.db.commit()
        self.db.refresh(q)
        return q

    def bulk_create(self, questions: List[dict]) -> List[Question]:
        objs = [Question(**q) for q in questions]
        self.db.bulk_save_objects(objs)
        self.db.commit()
        return objs

    def update(self, question_id: int, **kwargs) -> Optional[Question]:
        q = self.get_by_id(question_id)
        if not q:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(q, key, value)
        self.db.commit()
        self.db.refresh(q)
        return q

    def delete(self, question_id: int) -> bool:
        q = self.get_by_id(question_id)
        if not q:
            return False
        self.db.delete(q)
        self.db.commit()
        return True
