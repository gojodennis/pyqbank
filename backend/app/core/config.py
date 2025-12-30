from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PYQ Question Bank"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pyq_db"
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
