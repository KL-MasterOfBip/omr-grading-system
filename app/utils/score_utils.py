"""Score calculation utility functions."""
from typing import List


def calculate_percentage(score: float, max_score: float) -> float:
    """Return percentage score, 0 if max_score is 0."""
    if max_score == 0:
        return 0.0
    return round(score / max_score * 100, 2)


def to_10_scale(score: float, max_score: float) -> float:
    """Convert raw score to 10-point scale."""
    if max_score == 0:
        return 0.0
    return round(score / max_score * 10, 2)


def letter_grade(percentage: float) -> str:
    """Convert percentage to letter grade."""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"


def count_correct(answer_details: List[dict]) -> int:
    """Count number of correct answers from answer_details list."""
    return sum(1 for d in answer_details if d.get("is_correct"))
