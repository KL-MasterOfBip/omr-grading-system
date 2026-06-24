from PIL import Image, ImageDraw, ImageFont
import random

W, H = 600, 1600
NUM_QUESTIONS = 40
NUM_CHOICES   = 4

MARKER_SIZE = 30
MARGIN      = 20
START_X     = 180 + 20
START_Y     = 200 + 20 # đẩy xuống thêm vì có thêm vùng mã đề
COL_GAP     = 70
ROW_GAP     = 35
RADIUS      = 8

EXAM_CODE = random.choice(["101", "102", "103", "104"])
EXAM_CODES_ALL = ["101", "102", "103", "104"]

img  = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img)

# === 4 marker góc ===
for (x, y) in [
    (MARGIN, MARGIN),
    (W - MARGIN - MARKER_SIZE, MARGIN),
    (MARGIN, H - MARGIN - MARKER_SIZE),
    (W - MARGIN - MARKER_SIZE, H - MARGIN - MARKER_SIZE),
]:
    draw.rectangle([x, y, x+MARKER_SIZE, y+MARKER_SIZE], fill="black")
    print(x, y)
# === Font ===
# Thay dòng load font thành:
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
except:
    # Thử thêm path này nếu chạy trên Windows
    font_large = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)

# === Header thông tin ===
draw.text((MARGIN + 40, MARGIN + 5),  "PHIẾU TRẢ LỜI TRẮC NGHIỆM", font=font_large, fill="black")
draw.text((MARGIN + 40, MARGIN + 40), "Họ tên: ___________________________", font=font_small, fill="black")
draw.text((MARGIN + 40, MARGIN + 60), "MSSV:  ___________________________",  font=font_small, fill="black")

# === Vùng mã đề — ô tròn tô sẵn ===
CODE_X  = MARGIN + 40   # x bắt đầu vùng mã đề
CODE_Y  = MARGIN + 100  # y bắt đầu
CODE_GAP = 45           # khoảng cách ngang giữa các mã
R_CODE  = 10            # bán kính ô mã đề

draw.text((CODE_X, CODE_Y - 20), "Mã đề:", font=font_small, fill="black")

for idx, code in enumerate(EXAM_CODES_ALL):
    cx = CODE_X + idx * CODE_GAP + 40
    cy = CODE_Y + 10
    bbox = [cx - R_CODE, cy - R_CODE, cx + R_CODE, cy + R_CODE]

    if code == EXAM_CODE:
        draw.ellipse(bbox, fill="black")   # tô đặc = mã đề đang dùng
    else:
        draw.ellipse(bbox, outline="black")  # chỉ viền

    # Ghi số mã đề bên dưới ô
    draw.text((cx - 8, cy + R_CODE + 3), code, font=font_small, fill="black")

# === Header cột A B C D ===
for j, label in enumerate(["A", "B", "C", "D"]):
    cx = START_X + j * COL_GAP
    draw.text((cx - 4, START_Y - 22), label, font=font_small, fill="black")

# === 40 câu × 4 ô tròn ===
answers = []
for i in range(NUM_QUESTIONS):
    cy = START_Y + i * ROW_GAP
    chosen = random.randint(0, 3)
    answers.append(chosen)

    draw.text((MARGIN + 40, cy - 6), f"{i+1:2d}.", font=font_small, fill="black")

    for j in range(NUM_CHOICES):
        cx   = START_X + j * COL_GAP
        bbox = [cx-RADIUS, cy-RADIUS, cx+RADIUS, cy+RADIUS]
        if j == chosen:
            draw.ellipse(bbox, fill="black")
        else:
            draw.ellipse(bbox, outline="black")

img.save("samples/sample_sheet.png")
print(f"Mã đề: {EXAM_CODE}")
print(f"Đáp án: {[['A','B','C','D'][a] for a in answers]}")

print(f"START_X={START_X}, START_Y={START_Y}")
print(f"ROW_GAP={ROW_GAP}, COL_GAP={COL_GAP}")
print(f"Canvas W={W}, H={H}")
print(f"Marker TL góc ngoài: ({MARGIN}, {MARGIN})")
print(f"Marker BR góc ngoài: ({W-MARGIN}, {H-MARGIN})")