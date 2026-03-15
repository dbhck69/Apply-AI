import fitz  # PyMuPDF
from pathlib import Path

def parse_resume_pdf(file_bytes: bytes) -> str:
    """Extract clean text from a resume PDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    
    for page in doc:
        # Extract text with proper spacing
        text = page.get_text("text")
        text_parts.append(text)
    
    doc.close()
    full_text = "\n".join(text_parts)
    
    # Basic cleanup
    lines = [line.strip() for line in full_text.split("\n") if line.strip()]
    return "\n".join(lines)