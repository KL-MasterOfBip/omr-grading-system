from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import Base, engine
import app.models  # noqa: F401 — registers all models with SQLAlchemy before create_all
from app.routers import auth, exam, question, scan

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OMR System",
    description="Optical Mark Recognition System for exam grading",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(exam.router, prefix="/exams", tags=["exams"])
app.include_router(question.router, prefix="/questions", tags=["questions"])
app.include_router(scan.router, prefix="/scan", tags=["scan"])


@app.get("/")
async def root():
    return {"message": "OMR System API is running"}
