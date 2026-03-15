from dotenv import load_dotenv
load_dotenv()  # Load .env file into os.environ BEFORE anything else

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "applyai"
    DATABASE_URL: str = "sqlite:///./applyai.db"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    FRONTEND_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()