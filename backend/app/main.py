import io
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

from .analyzer import analyze_resume


app = FastAPI(title="PlacementAI API", version="1.0.0")
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "placement-ai-api"}


def extract_text(filename: str, content: bytes) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix == "pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise HTTPException(status_code=422, detail="The PDF could not be read.") from exc
    if suffix == "txt":
        return content.decode("utf-8", errors="ignore")
    raise HTTPException(status_code=415, detail="Upload a PDF or TXT resume.")


@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(default=""),
) -> dict:
    content = await resume.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume must be smaller than 5 MB.")
    text = extract_text(resume.filename or "resume", content)
    if len(text.strip()) < 40:
        raise HTTPException(status_code=422, detail="Not enough readable resume text was found.")
    return analyze_resume(text, job_description)

