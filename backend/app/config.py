from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    ALGORITHM: str = "HS256"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Integrated Ministry Operations Platform"
    
    class Config:
        env_file = ".env"

settings = Settings()
