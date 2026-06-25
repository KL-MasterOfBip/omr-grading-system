import cv2
import numpy as np
from typing import Dict

# Hằng số — phải khớp với generate_sheet.py
NUM_QUESTIONS  = 40
NUM_CHOICES    = 4
START_X        = 180 + 20
START_Y        = 200 + 20
COL_GAP        = 70
ROW_GAP        = 35
RADIUS         = 8
TOLERANCE      = 10
W, H           = 600, 1700
MARKER_SIZE    = 30
MARGIN         = 20
CODE_X         = 20 + 40
CODE_Y         = 20 + 100 + 10
CODE_GAP       = 45
R_CODE         = 10
EXAM_CODES_ALL = ["101", "102", "103", "104"]


def detect_answers(image_path: str) -> Dict[int, str]:
    """
    Đọc ảnh bài thi, trả về dict {question_order: answer_letter}.
    Đây là hàm được gọi bởi OMRService.
    """
    labels = ["A", "B", "C", "D"]
    try:
        img, thresh      = _preprocess(image_path)
        corners          = _find_corners(thresh)
        if corners is not None:
            warped, warped_thresh = _perspective_transform(img, thresh, corners)
        else:
            print("[WARN] Không tìm thấy đủ marker, dùng ảnh gốc")
            warped_thresh = thresh

        detected_indices = _read_omr(warped_thresh)  # list[int], index 0-3
        return {i + 1: labels[idx] for i, idx in enumerate(detected_indices)}

    except Exception as e:
        print(f"[OMR detect error] {e}")
        return {}


def _preprocess(img_path: str):
    img    = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Không đọc được ảnh: {img_path}")
    gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur   = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return img, thresh


def _find_corners(thresh):
    img_h, img_w = thresh.shape[:2]
    contours, _  = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates   = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if not (20 <= w <= 45 and 20 <= h <= 45 and abs(w - h) < 8):
            continue
        area     = cv2.contourArea(cnt)
        solidity = area / (w * h)
        if solidity < 0.85:
            continue
        cx = x + w // 2
        cy = y + h // 2
        in_left   = cx < img_w * 0.25
        in_right  = cx > img_w * 0.75
        in_top    = cy < img_h * 0.25
        in_bottom = cy > img_h * 0.75
        if not ((in_left or in_right) and (in_top or in_bottom)):
            continue
        candidates.append((x, y, w, h))

    if len(candidates) != 4:
        print(f"[WARN] Tìm được {len(candidates)} marker, cần 4!")
        return None

    candidates.sort(key=lambda m: (m[1], m[0]))
    top    = sorted(candidates[:2], key=lambda m: m[0])
    bottom = sorted(candidates[2:], key=lambda m: m[0])
    tl, tr, bl, br = top[0], top[1], bottom[0], bottom[1]

    def center(m): return [m[0] + m[2] // 2, m[1] + m[3] // 2]
    return np.float32([center(tl), center(tr), center(bl), center(br)])


def _perspective_transform(img, thresh, corners):
    MARKER_CENTER = MARGIN + MARKER_SIZE // 2
    dst = np.float32([
        [MARKER_CENTER,     MARKER_CENTER    ],
        [W - MARKER_CENTER, MARKER_CENTER    ],
        [MARKER_CENTER,     H - MARKER_CENTER],
        [W - MARKER_CENTER, H - MARKER_CENTER],
    ])
    M = cv2.getPerspectiveTransform(corners, dst)
    return (cv2.warpPerspective(img,    M, (W, H)),
            cv2.warpPerspective(thresh, M, (W, H)))


def _read_omr(warped_thresh) -> list:
    results = []
    for i in range(NUM_QUESTIONS):
        cy     = START_Y + i * ROW_GAP
        counts = []
        for j in range(NUM_CHOICES):
            cx = START_X + j * COL_GAP
            x1 = max(0, cx - TOLERANCE)
            y1 = max(0, cy - TOLERANCE)
            x2 = min(warped_thresh.shape[1], cx + TOLERANCE)
            y2 = min(warped_thresh.shape[0], cy + TOLERANCE)
            counts.append(cv2.countNonZero(warped_thresh[y1:y2, x1:x2]))
        results.append(int(np.argmax(counts)))
    return results