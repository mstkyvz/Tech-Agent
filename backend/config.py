from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = 'AIzaSyCNHaneKcsHabFH9PPxUYBWJ1cJldFshHg'
    DATABASE_URL: str = "sqlite:///./chat_history.db"
    
    class Config:
        env_file = ".env"

settings = Settings()