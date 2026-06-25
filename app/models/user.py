from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    admin   = "admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50),  unique=True, nullable=False, index=True)
    email         = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name     = Column(String(100), nullable=True)
    role          = Column(SAEnum(UserRole), default=UserRole.teacher, nullable=False)
    is_active     = Column(Boolean, default=True)
    is_superuser  = Column(Boolean, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())

    # Quan hệ: 1 teacher tạo nhiều exam, exam_codes, questions
    exams = relationship("Exam", back_populates="creator")
    exam_codes = relationship("ExamCode", back_populates="creator")
    questions = relationship("Question", back_populates="creator")