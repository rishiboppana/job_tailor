from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str
    DB_NAME: str = "resume_tailor"
    OLLAMA_URL: str = "http://localhost:11434"

settings = Settings()
