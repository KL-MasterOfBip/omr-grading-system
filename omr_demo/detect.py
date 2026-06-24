import cv2
import numpy as np
import time
import random

# ==========================================
# CẤU HÌNH
# ==========================================
NUM_QUESTIONS  = 40
NUM_CHOICES    = 4
START_X        = 180 + 20
START_Y        = 200 + 20
COL_GAP        = 70 
ROW_GAP        = 35
RADIUS         = 8
TOLERANCE      = 10
W, H           = 600, 1600
MARKER_SIZE    = 30   # phải khớp với generate_sheet.py
MARGIN         = 20   # phải khớp với generate_sheet.py

CODE_X         = 20 + 40
CODE_Y         = 20 + 100 + 10
CODE_GAP       = 45
R_CODE         = 10
EXAM_CODES_ALL = ["101", "102", "103", "104"]

GREEN = (0, 200, 0)

# ==========================================
# BƯỚC 0: KHAI BÁO ĐÁP ÁN ĐÚNG
# (sau này thay bằng nhận từ DB/API/file)
# ==========================================
def load_answer_key():
    key = [random.randint(0, 3) for _ in range(NUM_QUESTIONS)]
    return key

def print_answer_key(answer_key):
    labels = ["A", "B", "C", "D"]
    print("=" * 45)
    print("ĐÁP ÁN ĐÚNG (trước khi xử lý ảnh):")
    print("-" * 45)
    for i in range(0, NUM_QUESTIONS, 10):   # in 10 câu/hàng
        chunk = answer_key[i:i+10]
        nums  = " ".join(f"{i+j+1:2d}" for j in range(len(chunk)))
        ans   = "  ".join(labels[a] for a in chunk)
        print(f"  Câu {nums}")
        print(f"       {ans}")
    print("=" * 45)


# ==========================================
# PIPELINE XỬ LÝ ẢNH
# ==========================================
def preprocess(img_path):
    img    = cv2.imread(img_path)
    gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur   = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return img, thresh


def find_corners(thresh):
    img_h, img_w = thresh.shape[:2]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # --- Lọc 1: kích thước bounding rect phải gần vuông ---
        if not (20 <= w <= 45 and 20 <= h <= 45 and abs(w - h) < 8):
            continue

        # --- Lọc 2: solidity (độ đặc) — marker đặc nên solidity >= 0.85
        # solidity = diện tích contour thực / diện tích bounding rect
        # Hình tròn rỗng (ô bubble) có solidity thấp hơn nhiều
        area = cv2.contourArea(cnt)
        solidity = area / (w * h)
        if solidity < 0.85:
            continue

        # --- Lọc 3: marker phải nằm trong vùng 25% góc ảnh ---
        # Chia ảnh thành 4 góc, mỗi góc chiếm 25% chiều rộng và 25% chiều cao
        # Marker không thể nằm ở giữa ảnh
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
        print(f"[WARN] Tìm được {len(candidates)} marker hợp lệ, cần 4!")
        return None

    # Sắp xếp: top-left, top-right, bottom-left, bottom-right
    candidates.sort(key=lambda m: (m[1], m[0]))
    top    = sorted(candidates[:2], key=lambda m: m[0])
    bottom = sorted(candidates[2:], key=lambda m: m[0])
    tl, tr, bl, br = top[0], top[1], bottom[0], bottom[1]

    def center(m): return [m[0] + m[2] // 2, m[1] + m[3] // 2]
    corners = np.float32([center(tl), center(tr), center(bl), center(br)])
    print(f"[INFO] Markers (cx,cy): TL={corners[0]}, TR={corners[1]}, BL={corners[2]}, BR={corners[3]}")
    return corners

# Đưa về dạng xử lý chuẩn
def perspective_transform(img, thresh, corners):
    # Tâm của 4 marker sau khi warp phải khớp đúng với tọa độ marker
    # trong canvas gốc (generate_sheet.py): MARGIN + MARKER_SIZE//2 = 20 + 15 = 35
    MARKER_CENTER = MARGIN + MARKER_SIZE // 2   # = 35
    dst = np.float32([
        [MARKER_CENTER,     MARKER_CENTER    ],  # TL
        [W - MARKER_CENTER, MARKER_CENTER    ],  # TR
        [MARKER_CENTER,     H - MARKER_CENTER],  # BL
        [W - MARKER_CENTER, H - MARKER_CENTER],  # BR
    ])
    M = cv2.getPerspectiveTransform(corners, dst)
    return (cv2.warpPerspective(img,    M, (W, H)),
            cv2.warpPerspective(thresh, M, (W, H)))


def read_exam_code(warped_thresh):
    counts = []
    for idx in range(len(EXAM_CODES_ALL)):
        cx = CODE_X + idx * CODE_GAP + 40
        cy = CODE_Y
        x1 = max(0, cx - TOLERANCE)
        y1 = max(0, cy - TOLERANCE)
        x2 = min(warped_thresh.shape[1], cx + TOLERANCE)
        y2 = min(warped_thresh.shape[0], cy + TOLERANCE)
        counts.append(cv2.countNonZero(warped_thresh[y1:y2, x1:x2]))
    return EXAM_CODES_ALL[int(np.argmax(counts))]


def read_omr(warped_thresh):
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


def grade(detected, answer_key):
    """So sánh từng câu, trả về (điểm, list kết quả từng câu)"""
    detail = []
    for i, (d, a) in enumerate(zip(detected, answer_key)):
        detail.append({
            "cau"       : i + 1,
            "chon"      : d,
            "dung"      : a,
            "correct"   : d == a,
        })
    score = sum(1 for r in detail if r["correct"])
    return score, detail


def print_result(detail, score, exam_code):
    labels = ["A", "B", "C", "D"]
    print(f"\nMã đề detect: {exam_code}")
    print("-" * 45)
    print(f"{'Câu':<6} {'Đã chọn':<10} {'Đáp án':<10} {'Kết quả'}")
    print("-" * 45)
    for r in detail:
        mark = "✓" if r["correct"] else "✗"
        print(f"  {r['cau']:2d}     {labels[r['chon']]:<10} {labels[r['dung']]:<10} {mark}")
    print("-" * 45)
    print(f"Điểm: {score}/{NUM_QUESTIONS}  ({score/NUM_QUESTIONS*10:.1f}/10)")


def visualize(warped, detail, exam_code):
    labels = ["A", "B", "C", "D"]
    for idx, code in enumerate(EXAM_CODES_ALL):
        cx    = CODE_X + idx * CODE_GAP + 40
        cy    = CODE_Y
        if code == exam_code:
            cv2.circle(warped, (cx, cy), R_CODE + 3, GREEN, 2)

    for r in detail:
        i  = r["cau"] - 1
        cy = START_Y + i * ROW_GAP
        cx = START_X + r["chon"] * COL_GAP
        color = (0, 200, 0) if r["correct"] else (0, 0, 220)  # xanh=đúng, đỏ=sai
        cv2.circle(warped, (cx, cy), RADIUS + 4, color, 2)
        cv2.putText(warped, labels[r["chon"]],
                    (cx + 14, cy + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, color, 1)
    return warped


def process_one(img_path, answer_key):
    timing = {}
    t0 = time.perf_counter()

    img, thresh = preprocess(img_path)
    timing["preprocess"] = time.perf_counter() - t0

    t1 = time.perf_counter()
    corners = find_corners(thresh)
    if corners is not None:
        warped, warped_thresh = perspective_transform(img, thresh, corners)
    else:
        warped, warped_thresh = img, thresh
    timing["transform"] = time.perf_counter() - t1

    t2 = time.perf_counter()
    exam_code = read_exam_code(warped_thresh)
    timing["read_code"] = time.perf_counter() - t2

    t3 = time.perf_counter()
    detected = read_omr(warped_thresh)
    timing["omr"] = time.perf_counter() - t3

    t4 = time.perf_counter()
    score, detail = grade(detected, answer_key)
    timing["grade"] = time.perf_counter() - t4

    timing["total"] = time.perf_counter() - t0
    return detected, score, detail, exam_code, warped, timing

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    IMG_PATH = "samples/sample_sheet.png"

    # BƯỚC 0: load và thông báo đáp án trước
    answer_key = load_answer_key()
    print_answer_key(answer_key)

    # BƯỚC 1-5: xử lý ảnh
    detected, score, detail, exam_code, warped, timing = process_one(IMG_PATH, answer_key)

    # In kết quả chi tiết
    print_result(detail, score, exam_code)

    print(f"\n=== TIMING ===")
    for k, v in timing.items():
        print(f"  {k:12s}: {v*1000:.2f} ms")

    out = visualize(warped, detail, exam_code)
    cv2.imwrite("results/result.png", out)
    print("\nĐã lưu: results/result.png")