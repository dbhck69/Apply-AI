from pydantic import BaseModel, Field
from typing import Optional, List, TypedDict, Annotated
from enum import Enum
import operator

class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"

class JobProfile(BaseModel):
    title: str
    company: str
    required_skills: List[str]
    nice_to_have: List[str]
    experience_level: str
    tech_stack: List[str]
    culture_keywords: List[str]
    raw_text: str

class ApplicationState(TypedDict, total=False):
    """LangGraph state — passed between all agents"""
    run_id: str
    resume_text: str
    job_url: str
    job_text: str
    job_profile: Optional[dict]
    optimized_resume: str
    cover_letter: str
    cold_email: str
    errors: Annotated[list, operator.add]
    status: str

class RunRequest(BaseModel):
    job_url: str
    user_preferences: Optional[str] = "professional, concise"

class RunResponse(BaseModel):
    run_id: str
    status: str
    cover_letter: str = ""
    optimized_resume: str = ""
    cold_email: str = ""
    errors: List[str] = []