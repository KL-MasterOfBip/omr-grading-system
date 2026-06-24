"""PDF export service — generates a graded result PDF."""
import io
from typing import Optional

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as pdf_canvas
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def generate_result_pdf(
    student_name: Optional[str],
    student_id: Optional[str],
    exam_title: str,
    total_score: float,
    max_score: float,
    answer_details: list,
) -> bytes:
    """Generate a PDF result sheet and return raw bytes."""
    if not HAS_REPORTLAB:
        raise RuntimeError("reportlab is not installed. Run: pip install reportlab")

    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Kết quả: {exam_title}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Học sinh: {student_name or 'N/A'}  |  SBD: {student_id or 'N/A'}")
    c.drawString(50, height - 100, f"Điểm: {total_score} / {max_score}")

    y = height - 130
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Câu")
    c.drawString(100, y, "Đáp án chọn")
    c.drawString(200, y, "Đúng/Sai")
    y -= 20

    c.setFont("Helvetica", 10)
    for i, detail in enumerate(answer_details, start=1):
        c.drawString(50, y, str(i))
        c.drawString(100, y, detail.get("selected_answer") or "-")
        c.drawString(200, y, "✓" if detail.get("is_correct") else "✗")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return buffer.getvalue()
