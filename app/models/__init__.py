# models package — import all models so SQLAlchemy registers them before create_all
from app.models.user import User  # noqa: F401
from app.models.exam import Exam  # noqa: F401
from app.models.exam_code import ExamCode  # noqa: F401
from app.models.question import Question  # noqa: F401
from app.models.scan_result import ScanResult  # noqa: F401
from app.models.answer_detail import AnswerDetail  # noqa: F401
