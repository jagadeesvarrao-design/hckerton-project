import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Passport Seva AI 2.0 (High-Concurrency Engine)"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "2.0.0"
    
    # Concurrency & Performance
    WORKERS_COUNT: int = 4
    MAX_CONNECTIONS: int = 100000
    CACHE_TTL_SECONDS: int = 3600
    
    # OpenAI & LLM Config (Custom Endpoint / Key Support)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL", None) # Allows custom API links / proxies
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Security & CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:8088",
        "http://localhost:8099",
        "https://buildwhatmovesindia.com",
        "*"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
