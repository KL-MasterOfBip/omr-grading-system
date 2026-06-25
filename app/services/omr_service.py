import os
import uuid
import numpy as np
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.omr.detect import detect_answers
from app.services.grading_service import GradingService
from app.repositories.result_repository import ResultRepository
from app.repositories.question_repository import QuestionRepository
from app.models.exam_code import ExamCode


class OMRService:
    def __init__(self, db: Session):
        self.db = db
        self.result_repo = ResultRepository(db)
        self.question_repo = QuestionRepository(db)
        self.grading_service = GradingService(db)

    def process_image(
        self,
        exam_code_id: int,
        image_bytes: bytes,
        filename: Optional[str] = None,
        student_id: Optional[str] = None,
        student_name: Optional[str] = None,
    ):
        """
        Main pipeline:
        1. Save image to disk
        2. Run OMR detection
        3. Grade answers
        4. Persist result
        """
        # 1. Save image
        upload_dir = os.path.join(settings.UPLOAD_DIR, str(exam_code_id))
        os.makedirs(upload_dir, exist_ok=True)
        unique_name = f"{uuid.uuid4().hex}_{filename or 'scan.jpg'}"
        image_path = os.path.join(upload_dir, unique_name)
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # 2. Detect OMR answers
        detected_answers = detect_answers(image_path)  # dict: {question_order: answer}

        # 3. Grade
        questions = self.question_repo.get_by_exam_code(exam_code_id)
        total_score, max_score, answer_details = self.grading_service.grade(
            questions=questions,
            detected_answers=detected_answers,
        )

        # 4. Save result
        exam_code_obj = self.db.query(ExamCode).filter(ExamCode.id == exam_code_id).first()
        exam_id = exam_code_obj.exam_id if exam_code_obj else 0

        result = self.result_repo.create_result(
            exam_id=exam_id,
            exam_code_id=exam_code_id,
            student_id=student_id,
            student_name=student_name,
            image_path=image_path,
            total_score=total_score,
            max_score=max_score,
        )
        # Save per-question answers
        answer_rows = [
            {
                "scan_result_id": result.id,
                "question_id": detail["question_id"],
                "selected_answer": detail["selected_answer"],
                "is_correct": detail["is_correct"],
            }
            for detail in answer_details
        ]
        self.result_repo.bulk_create_answers(answer_rows)

        return result
