from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ExamCode(Base):
    """Mỗi đề thi có thể có nhiều mã đề (A, B, C, D...)."""
    __tablename__ = "exam_codes"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    code = Column(String, nullable=False)  # e.g. "001", "002"
    description = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    exam = relationship("Exam", back_populates="exam_codes")
    creator = relationship("User", back_populates="exam_codes")
    questions = relationship("Question", back_populates="exam_code", cascade="all, delete-orphan")
