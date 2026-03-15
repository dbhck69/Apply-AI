from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import ApplicationState

COVER_LETTER_PROMPT = ChatPromptTemplate.from_template("""
Write a compelling, personalized cover letter for this job application.

CANDIDATE PROFILE (from their resume):
{resume_text}

JOB DETAILS:
- Role: {title} at {company}
- Key Requirements: {required_skills}
- Company Culture: {culture_keywords}

INSTRUCTIONS:
- 3 paragraphs, max 300 words
- Opening: Hook with genuine excitement + 1 specific company insight
- Middle: 2-3 concrete achievements directly matching their requirements
- Closing: Clear call to action
- Tone: Confident but not arrogant. Human, not corporate.
- NO generic phrases like "I am writing to apply..." or "Please find attached"
""")

COLD_EMAIL_PROMPT = ChatPromptTemplate.from_template("""
Write a short, effective cold outreach email to the hiring manager for this role.

Role: {title} at {company}
Candidate's strongest relevant skill: {top_skill}

Requirements:
- Subject line: compelling, under 8 words
- Body: 4-5 sentences max
- Reference the specific role and ONE specific thing about the company
- End with a clear, low-friction ask
- Format: Subject: [line] \\n\\n [body]
""")

async def writer_node(state: ApplicationState) -> dict:
    """LangGraph node: write cover letter and cold email."""
    job_profile = state.get("job_profile")
    errors = state.get("errors", [])
    
    if not job_profile or errors:
        return {"cover_letter": "", "cold_email": ""}
    
    try:
        # Use llama-3.3-70b for best writing quality on Groq
        llm_writer = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        
        # Cover letter
        cover_chain = COVER_LETTER_PROMPT | llm_writer
        cover = await cover_chain.ainvoke({
            "resume_text": state.get("optimized_resume", "")[:2000],
            "title": job_profile.get("title", ""),
            "company": job_profile.get("company", ""),
            "required_skills": ", ".join(job_profile.get("required_skills", [])[:5]),
            "culture_keywords": ", ".join(job_profile.get("culture_keywords", [])),
        })
        cover_letter = cover.content
        
        # Cold email
        email_chain = COLD_EMAIL_PROMPT | llm_writer
        req_skills = job_profile.get("required_skills", [])
        email = await email_chain.ainvoke({
            "title": job_profile.get("title", ""),
            "company": job_profile.get("company", ""),
            "top_skill": req_skills[0] if req_skills else "software engineering",
        })
        cold_email = email.content
        
        return {"cover_letter": cover_letter, "cold_email": cold_email}
    except Exception as e:
        return {"errors": [f"Writer agent failed: {str(e)}"]}