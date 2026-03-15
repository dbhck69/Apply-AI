from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.schemas import ApplicationState, JobProfile

ANALYST_PROMPT = ChatPromptTemplate.from_template("""
You are an expert technical recruiter. Analyze this job posting and extract structured information.

Job Posting Text:
{job_text}

Return a JSON object with EXACTLY these fields:
- title: job title (string)
- company: company name (string)  
- required_skills: list of must-have technical skills (list of strings)
- nice_to_have: list of preferred skills (list of strings)
- experience_level: "junior" / "mid" / "senior" / "lead" (string)
- tech_stack: specific technologies mentioned (list of strings)
- culture_keywords: values/culture words mentioned (list of strings)
- raw_text: first 500 chars of job text (string)

Return ONLY valid JSON, no markdown, no code fences.
""")

async def job_analyst_node(state: ApplicationState) -> dict:
    """LangGraph node: analyze job posting."""
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        parser = JsonOutputParser(pydantic_object=JobProfile)
        chain = ANALYST_PROMPT | llm | parser
        job_text = state.get("job_text", "")
        result = await chain.ainvoke({"job_text": job_text[:4000]})
        return {"job_profile": result}
    except Exception as e:
        return {"errors": [f"Job analyst failed: {str(e)}"]}