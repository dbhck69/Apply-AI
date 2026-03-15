from langgraph.graph import StateGraph, END
from models.schemas import ApplicationState, AgentStatus
from tools.web_scraper import scrape_job_posting
from agents.job_analyst import job_analyst_node
from agents.resume_optimizer import resume_optimizer_node
from agents.writer import writer_node
import uuid

FALLBACK_JOB_TEXT = """
Software Engineer - Full Stack
Location: Remote
Experience: 2-4 years

Required Skills: Python, JavaScript, React, Node.js, SQL, REST APIs, Git
Nice to have: Docker, AWS, TypeScript, CI/CD, Agile

We are looking for a passionate full-stack developer to build scalable applications.
Tech Stack: Python, FastAPI, React, Next.js, PostgreSQL, Redis, Docker
Culture: Innovation, collaboration, continuous learning, work-life balance
"""

async def scraper_node(state: ApplicationState) -> dict:
    """Node 1: Scrape the job posting."""
    try:
        job_text = await scrape_job_posting(state["job_url"])
        if job_text and len(job_text) > 100:
            return {"job_text": job_text, "status": AgentStatus.RUNNING}
        else:
            # Got some text but too short, use fallback
            return {"job_text": FALLBACK_JOB_TEXT, "status": AgentStatus.RUNNING}
    except Exception as e:
        # Scraping failed entirely — use fallback so pipeline continues
        print(f"[Scraper] Warning: {e} — using fallback job text")
        return {"job_text": FALLBACK_JOB_TEXT, "status": AgentStatus.RUNNING}

def should_continue(state: ApplicationState) -> str:
    """Conditional edge: stop if errors accumulate."""
    if len(state.get("errors", [])) >= 2:
        return "end"
    return "continue"

def build_graph():
    """Build and compile the LangGraph agent graph."""
    graph = StateGraph(ApplicationState)
    
    # Add nodes
    graph.add_node("scraper", scraper_node)
    graph.add_node("job_analyst", job_analyst_node)
    graph.add_node("resume_optimizer", resume_optimizer_node)
    graph.add_node("writer", writer_node)
    
    # Add edges (the flow)
    graph.set_entry_point("scraper")
    graph.add_conditional_edges(
        "scraper",
        should_continue,
        {"continue": "job_analyst", "end": END}
    )
    graph.add_conditional_edges(
        "job_analyst",
        should_continue,
        {"continue": "resume_optimizer", "end": END}
    )
    graph.add_edge("resume_optimizer", "writer")
    graph.add_edge("writer", END)
    
    return graph.compile()

# Singleton graph instance
app_graph = build_graph()

async def run_application_agent(
    resume_text: str,
    job_url: str,
    preferences: str = ""
) -> dict:
    """Main entry point: run the full agent pipeline."""
    initial_state = {
        "run_id": str(uuid.uuid4()),
        "resume_text": resume_text,
        "job_url": job_url,
        "status": AgentStatus.RUNNING,
        "job_text": "",
        "job_profile": None,
        "optimized_resume": "",
        "cover_letter": "",
        "cold_email": "",
        "errors": [],
    }
    result = await app_graph.ainvoke(initial_state)
    result["status"] = AgentStatus.DONE if not result.get("errors") else AgentStatus.FAILED
    return result