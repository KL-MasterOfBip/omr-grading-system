# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base

from app.models import user, exam, exam_code, question, scan_result, answer_detail  # noqa: F401

# Import routers
from app.routers import auth, exam, question, scan, exam_code

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,   
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(auth.router,     prefix="/auth",      tags=["auth"])
app.include_router(exam.router,     prefix="/exams",     tags=["exams"])
app.include_router(question.router, prefix="/questions", tags=["questions"])
app.include_router(scan.router,     prefix="/scan",      tags=["scan"])
app.include_router(exam_code.router, prefix="/exam-codes", tags=["exam-codes"])

# Frontend Pages Router
from app.routers import pages
app.include_router(pages.router)

# Mount static files & uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
