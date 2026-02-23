from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Application Backend"
    PROJECT_VERSION: str = "1.0.0"

    # Database Configuration (Must be defined in .env or Environment)
    DB_HOST: str 
    DB_PORT: int 
    DB_USER: str 
    DB_PASSWORD: str 
    DB_NAME: str 

    # API Keys (Required in production, no defaults)
    GROQ_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None

    # JWT Configuration
    SECRET_KEY: str = "temporary-secret-key-change-this-in-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours
    MASTER_BEARER_TOKEN: str = "master-key-must-be-set-in-env"

    MAX_TOKEN_LIMIT: int = 32000
    AI_MAX_OUTPUT_TOKENS: int = 8000

    # Frontend Bearer Token (Long-lived) - MUST be set in environment variables
    FRONTEND_BEARER_TOKEN: Optional[str] = None

    # Security: Allowed Hosts for TrustedHostMiddleware
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "*.onrender.com", "192.168.0.125"]

    @property
    def DATABASE_URL(self) -> str:
        from urllib.parse import quote_plus
        # Handle cases where DB settings might be None or empty strings
        if not self.DB_PASSWORD:
            return f"mysql+pymysql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"mysql+pymysql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
