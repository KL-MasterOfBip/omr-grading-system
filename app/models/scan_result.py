from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    exam_code_id = Column(Integer, ForeignKey("exam_codes.id"), nullable=True)
    student_id = Column(String, nullable=True)    # Mã học sinh / SBD
    student_name = Column(String, nullable=True)
    image_path = Column(String, nullable=True)    # Đường dẫn ảnh bài thi
    total_score = Column(Float, default=0.0)
    max_score = Column(Float, default=0.0)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    # Relationships
    exam = relationship("Exam", back_populates="scan_results")
    exam_code = relationship("ExamCode")
    answer_details = relationship("AnswerDetail", back_populates="scan_result", cascade="all, delete-orphan")
