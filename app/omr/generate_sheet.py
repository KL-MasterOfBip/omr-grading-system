from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import random

W, H = 600, 1700
NUM_QUESTIONS  = 40
NUM_CHOICES    = 4
MARKER_SIZE    = 30
MARGIN         = 20
START_X        = 180 + 20
START_Y        = 200 + 20
COL_GAP        = 70
ROW_GAP        = 35
RADIUS         = 8
EXAM_CODES_ALL = ["101", "102", "103", "104"]
CODE_X         = MARGIN + 40
CODE_Y         = MARGIN + 100
CODE_GAP       = 45
R_CODE         = 10


def _load_fonts():
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except:
        font_large = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    return font_large, font_small


def generate_sheet(
    exam_code: Optional[str] = None,
    output_path: Optional[str] = None,
    randomize_answers: bool = False,
) -> tuple:
    """
    Tạo ảnh phiếu trả lời trắc nghiệm.
    
    Returns:
        (img, answers, exam_code)
        - img: PIL Image
        - answers: list[int] đáp án đã tô (0-3), rỗng nếu randomize_answers=False
        - exam_code: mã đề thực sự dùng
    """
    if exam_code is None:
        exam_code = random.choice(EXAM_CODES_ALL)

    img  = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font_large, font_small = _load_fonts()

    # 4 marker góc
    for (x, y) in [
        (MARGIN, MARGIN),
        (W - MARGIN - MARKER_SIZE, MARGIN),
        (MARGIN, H - MARGIN - MARKER_SIZE),
        (W - MARGIN - MARKER_SIZE, H - MARGIN - MARKER_SIZE),
    ]:
        draw.rectangle([x, y, x + MARKER_SIZE, y + MARKER_SIZE], fill="black")

    # Header
    draw.text((MARGIN + 40, MARGIN + 5),  "PHIẾU TRẢ LỜI TRẮC NGHIỆM", font=font_large, fill="black")
    draw.text((MARGIN + 40, MARGIN + 40), "Họ tên: ___________________________", font=font_small, fill="black")
    draw.text((MARGIN + 40, MARGIN + 60), "MSSV:   ___________________________", font=font_small, fill="black")

    # Vùng mã đề
    draw.text((CODE_X, CODE_Y - 20), "Mã đề:", font=font_small, fill="black")
    for idx, code in enumerate(EXAM_CODES_ALL):
        cx   = CODE_X + idx * CODE_GAP + 40
        cy   = CODE_Y + 10
        bbox = [cx - R_CODE, cy - R_CODE, cx + R_CODE, cy + R_CODE]
        if code == exam_code:
            draw.ellipse(bbox, fill="black")
        else:
            draw.ellipse(bbox, outline="black")
        draw.text((cx - 8, cy + R_CODE + 3), code, font=font_small, fill="black")

    # Header cột A B C D
    for j, label in enumerate(["A", "B", "C", "D"]):
        cx = START_X + j * COL_GAP
        draw.text((cx - 4, START_Y - 22), label, font=font_small, fill="black")

    # 40 câu
    answers = []
    for i in range(NUM_QUESTIONS):
        cy     = START_Y + i * ROW_GAP
        chosen = random.randint(0, 3) if randomize_answers else None
        answers.append(chosen)
        draw.text((MARGIN + 40, cy - 6), f"{i+1:2d}.", font=font_small, fill="black")
        for j in range(NUM_CHOICES):
            cx   = START_X + j * COL_GAP
            bbox = [cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS]
            if chosen is not None and j == chosen:
                draw.ellipse(bbox, fill="black")
            else:
                draw.ellipse(bbox, outline="black")

    if output_path:
        img.save(output_path)

    return img, answers, exam_code

if __name__ == "__main__":
    generate_sheet(exam_code="101", output_path="./samples/answer_sheet_template.png", randomize_answers=True)