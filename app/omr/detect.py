"""
OMR detection module.
Replace the stub logic below with your actual OpenCV / image processing code.
"""
import cv2
import numpy as np
from typing import Dict


def detect_answers(image_path: str) -> Dict[int, str]:
    """
    Read an answer sheet image and return detected answers.

    Args:
        image_path: Path to the scanned image.

    Returns:
        A dict mapping question_order (1-indexed) → selected answer letter ("A"/"B"/"C"/"D").
        Returns empty dict on failure.
    """
    choices = ["A", "B", "C", "D"]
    detected: Dict[int, str] = {}

    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")

        # ── TODO: Replace with real bubble detection ──────────────────────
        # Example stub: pretend all answers are "A"
        # In production, use contour detection + bubble fill ratio analysis.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ... (your real OMR processing here) ...
        # ─────────────────────────────────────────────────────────────────

    except Exception as e:
        print(f"[OMR detect error] {e}")

    return detected


def preprocess_image(img: np.ndarray) -> np.ndarray:
    """Standard preprocessing: grayscale → blur → threshold."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh
