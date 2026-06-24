"""Image utility functions."""
import os
import uuid
import cv2
import numpy as np
from typing import Optional, Tuple


def save_upload(image_bytes: bytes, directory: str, original_name: Optional[str] = None) -> str:
    """Save raw bytes to disk with a unique filename. Returns the saved path."""
    os.makedirs(directory, exist_ok=True)
    ext = os.path.splitext(original_name or "img.jpg")[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(directory, filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path


def resize_image(img: np.ndarray, width: int = 800) -> np.ndarray:
    """Resize keeping aspect ratio."""
    h, w = img.shape[:2]
    ratio = width / w
    return cv2.resize(img, (width, int(h * ratio)))


def rotate_image(img: np.ndarray, angle: float) -> np.ndarray:
    """Rotate image by given angle (degrees)."""
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))


def to_grayscale(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def threshold_image(gray: np.ndarray) -> np.ndarray:
    """Otsu's thresholding."""
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh
