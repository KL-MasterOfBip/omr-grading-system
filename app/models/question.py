from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_code_id = Column(Integer, ForeignKey("exam_codes.id"), nullable=False)
    order = Column(Integer, nullable=False)          # Câu số bao nhiêu
    correct_answer = Column(String(1), nullable=False)  # A / B / C / D
    score = Column(Integer, default=1)               # Điểm mỗi câu
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    exam_code = relationship("ExamCode", back_populates="questions")
    creator = relationship("User", back_populates="questions")
    answer_details = relationship("AnswerDetail", back_populates="question")
