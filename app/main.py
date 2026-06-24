from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base

# Import tất cả models để SQLAlchemy nhận diện trước khi create_all
from app.models import user, exam, exam_code, question, scan_result, answer_detail  # noqa: F401

# Import routers
from app.routers import auth

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


@app.on_event("startup")
def on_startup():
    """Tạo tất cả bảng khi app khởi động (nếu chưa có)"""
    Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}