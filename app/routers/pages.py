from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")

# Disable Jinja2 bytecode caching (fix for Python 3.14+ compatibility)
templates.env.auto_reload = True


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "auth/register.html")


@router.get("/exams", response_class=HTMLResponse)
async def exams_page(request: Request):
    return templates.TemplateResponse(request, "exam/list.html")


@router.get("/exams/{exam_id}", response_class=HTMLResponse)
async def exam_detail_page(request: Request, exam_id: int):
    return templates.TemplateResponse(request, "exam/detail.html", {"exam_id": exam_id})


@router.get("/scan", response_class=HTMLResponse)
async def scan_page(request: Request):
    return templates.TemplateResponse(request, "scan/upload.html")


@router.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse(request, "scan/result.html")
