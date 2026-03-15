from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from tools.pdf_parser import parse_resume_pdf
from agents.orchestrator import run_application_agent
from models.schemas import RunResponse, AgentStatus

router = APIRouter(prefix="/api/v1")

@router.post("/apply", response_model=RunResponse)
async def create_application(
    resume: UploadFile = File(...),
    job_url: str = Form(...),
    preferences: str = Form(default="professional, concise")
):
    """Main endpoint: upload resume + job URL → get tailored application."""
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(400, "Resume must be a PDF file")
    
    # Parse resume
    file_bytes = await resume.read()
    resume_text = parse_resume_pdf(file_bytes)
    
    if len(resume_text) < 100:
        raise HTTPException(400, "Could not extract text from resume PDF")
    
    # Run agent pipeline
    result = await run_application_agent(
        resume_text=resume_text,
        job_url=job_url,
        preferences=preferences
    )
    
    return RunResponse(
        run_id=result["run_id"],
        status=result["status"],
        cover_letter=result.get("cover_letter", ""),
        optimized_resume=result.get("optimized_resume", ""),
        cold_email=result.get("cold_email", ""),
        errors=result.get("errors", [])
    )

@router.get("/health")
async def health():
    return {"status": "ok", "service": "ApplyAI"}