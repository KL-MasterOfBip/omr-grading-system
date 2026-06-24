from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services.omr_service import OMRService
from app.repositories.result_repository import ResultRepository
from app.schemas.scan_result import ScanResultResponse

router = APIRouter()


@router.post("/upload/{exam_id}", response_model=ScanResultResponse, status_code=201)
async def scan_answer_sheet(
    exam_id: int,
    file: UploadFile = File(...),
    student_id: str = Form(None),
    student_name: str = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Upload and process an OMR answer sheet image."""
    contents = await file.read()
    omr_service = OMRService(db)
    result = omr_service.process_image(
        exam_id=exam_id,
        image_bytes=contents,
        filename=file.filename,
        student_id=student_id,
        student_name=student_name,
    )
    return result


@router.get("/results/{exam_id}", response_model=List[ScanResultResponse])
def get_results(exam_id: int, db: Session = Depends(get_db)):
    repo = ResultRepository(db)
    return repo.get_results_by_exam(exam_id)


@router.get("/result/{result_id}", response_model=ScanResultResponse)
def get_result(result_id: int, db: Session = Depends(get_db)):
    repo = ResultRepository(db)
    result = repo.get_result_by_id(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.delete("/result/{result_id}", status_code=204)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    repo = ResultRepository(db)
    if not repo.delete_result(result_id):
        raise HTTPException(status_code=404, detail="Result not found")
