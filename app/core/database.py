from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


# ── Engine ─────────────────────────────────────────────────────────────────
# connect_args chỉ cần thiết với SQLite (không hỗ trợ multi-thread mặc định)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# ── Session factory ────────────────────────────────────────────────────────
# autocommit=False → phải gọi db.commit() thủ công (kiểm soát transaction rõ ràng hơn)
# autoflush=False  → không tự flush trước mỗi query (tránh side-effect bất ngờ)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Base class cho tất cả models ───────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Dependency dùng trong FastAPI router ───────────────────────────────────
# Mỗi request sẽ có 1 session riêng, tự đóng sau khi xong
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()