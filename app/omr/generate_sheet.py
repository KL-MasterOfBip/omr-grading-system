"""
Generate OMR answer sheet as an image or PDF.
Replace / extend with your real sheet layout logic.
"""
from typing import Optional
import numpy as np


def generate_sheet(
    num_questions: int = 40,
    num_choices: int = 4,
    exam_title: str = "Bài thi",
    exam_code: Optional[str] = None,
    output_path: Optional[str] = None,
) -> np.ndarray:
    """
    Generate a blank OMR answer sheet image.

    Args:
        num_questions: Number of questions.
        num_choices: Number of choices per question (e.g. 4 for A-B-C-D).
        exam_title: Title printed at the top of the sheet.
        exam_code: Exam code / mã đề.
        output_path: If provided, save the image to this path.

    Returns:
        numpy array (BGR image).
    """
    try:
        import cv2
    except ImportError:
        raise RuntimeError("opencv-python is required: pip install opencv-python")

    height = 80 + num_questions * 20 + 40
    width = 600
    sheet = np.ones((height, width, 3), dtype=np.uint8) * 255  # white background

    # Title
    cv2.putText(sheet, exam_title, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    if exam_code:
        cv2.putText(sheet, f"Ma de: {exam_code}", (400, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # Draw bubbles
    choice_labels = [chr(ord("A") + i) for i in range(num_choices)]
    start_y = 60
    for q in range(num_questions):
        y = start_y + q * 20
        cv2.putText(sheet, f"{q + 1:2d}.", (10, y + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        for c, label in enumerate(choice_labels):
            cx = 60 + c * 50
            cv2.circle(sheet, (cx, y + 7), 8, (0, 0, 0), 1)
            cv2.putText(sheet, label, (cx - 4, y + 11), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

    if output_path:
        cv2.imwrite(output_path, sheet)

    return sheet
