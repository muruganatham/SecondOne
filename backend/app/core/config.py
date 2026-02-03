from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Application Backend"
    PROJECT_VERSION: str = "1.0.0"

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "Varun1121@#"
    DB_NAME: str = "coderv4"

    # API Keys
    GROQ_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-for-jwt-generation-should-be-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours

    MAX_TOKEN_LIMIT: int = 4096

    @property
    def DATABASE_URL(self) -> str:
        from urllib.parse import quote_plus
        # Handle cases where DB settings might be None or empty strings if loaded from env strangely, 
        # though defaults are provided above.
        return f"mysql+pymysql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
