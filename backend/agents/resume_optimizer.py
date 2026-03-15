from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import ApplicationState

OPTIMIZER_PROMPT = ChatPromptTemplate.from_template("""
You are an expert ATS-optimized resume writer and career coach.

CANDIDATE'S CURRENT RESUME:
{resume_text}

TARGET JOB PROFILE:
- Title: {job_title} at {company}
- Required Skills: {required_skills}
- Tech Stack: {tech_stack}
- Experience Level: {experience_level}

YOUR TASK:
1. Rewrite the work experience bullet points to mirror the job's language
2. Ensure ALL required skills that the candidate has are prominently mentioned
3. Use STAR format (Situation, Task, Action, Result) for impact bullets
4. Add quantified metrics where possible (even estimates)
5. Keep it truthful — only enhance what's already there, don't fabricate

Return the full optimized resume text, ready to paste.
""")

async def resume_optimizer_node(state: ApplicationState) -> dict:
    """LangGraph node: optimize resume for the target job."""
    job_profile = state.get("job_profile")
    errors = state.get("errors", [])
    
    if not job_profile or errors:
        return {"optimized_resume": state.get("resume_text", "")}
    
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
        chain = OPTIMIZER_PROMPT | llm
        result = await chain.ainvoke({
            "resume_text": state.get("resume_text", ""),
            "job_title": job_profile.get("title", ""),
            "company": job_profile.get("company", ""),
            "required_skills": ", ".join(job_profile.get("required_skills", [])),
            "tech_stack": ", ".join(job_profile.get("tech_stack", [])),
            "experience_level": job_profile.get("experience_level", ""),
        })
        return {"optimized_resume": result.content}
    except Exception as e:
        return {"errors": [f"Resume optimizer failed: {str(e)}"]}