from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.scan_result import ScanResult
from app.models.answer_detail import AnswerDetail


class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── ScanResult ──────────────────────────────────────────────────────────

    def get_result_by_id(self, result_id: int) -> Optional[ScanResult]:
        return self.db.query(ScanResult).filter(ScanResult.id == result_id).first()

    def get_results_by_exam(self, exam_id: int) -> List[ScanResult]:
        return self.db.query(ScanResult).filter(ScanResult.exam_id == exam_id).all()

    def create_result(self, **kwargs) -> ScanResult:
        result = ScanResult(**kwargs)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def delete_result(self, result_id: int) -> bool:
        result = self.get_result_by_id(result_id)
        if not result:
            return False
        self.db.delete(result)
        self.db.commit()
        return True

    # ── AnswerDetail ─────────────────────────────────────────────────────────

    def bulk_create_answers(self, answers: List[dict]) -> List[AnswerDetail]:
        objs = [AnswerDetail(**a) for a in answers]
        self.db.bulk_save_objects(objs)
        self.db.commit()
        return objs

    def get_answers_by_result(self, result_id: int) -> List[AnswerDetail]:
        return (
            self.db.query(AnswerDetail)
            .filter(AnswerDetail.scan_result_id == result_id)
            .all()
        )
