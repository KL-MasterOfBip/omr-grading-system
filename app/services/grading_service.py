from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models.question import Question


class GradingService:
    def __init__(self, db: Session):
        self.db = db

    def grade(
        self,
        questions: List[Question],
        detected_answers: Dict[int, str],
    ) -> Tuple[float, float, List[dict]]:
        """
        Compare detected answers against correct answers.

        Returns:
            total_score: float
            max_score: float
            answer_details: list of dicts with question_id, selected_answer, is_correct
        """
        total_score = 0.0
        max_score = 0.0
        answer_details = []

        for question in questions:
            max_score += question.score
            selected = detected_answers.get(question.order)
            is_correct = selected == question.correct_answer
            if is_correct:
                total_score += question.score

            answer_details.append(
                {
                    "question_id": question.id,
                    "selected_answer": selected,
                    "is_correct": is_correct,
                }
            )

        return total_score, max_score, answer_details
