from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Application Backend"
    PROJECT_VERSION: str = "1.0.0"

    # Database Configuration (Must be defined in .env or Environment)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "Varun1121@#"
    DB_NAME: str = "coderv4"

    # API Keys (Required in production, no defaults)
    GROQ_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # JWT Configuration
    SECRET_KEY: str = "temporary-secret-key-change-this-in-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours
    MASTER_API_KEY: str = "master-key-must-be-set-in-env"

    MAX_TOKEN_LIMIT: int = 4096

    # Frontend Static Token (Long-lived)
    FRONTEND_STATIC_TOKEN: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImZyb250ZW5kLWFwcCIsInR5cGUiOiJsb25nLWxpdmVkIiwiZ2VuZXJhdGVkIjoiMjAyNS0xMi0yMlQwNToyNzo0My41NTdaIiwiZGVzY3JpcHRpb24iOiJMb25nLWxpdmVkIHRva2VuIGZvciBmcm9udGVuZCBoYXJkY29kZWQgYXV0aGVudGljYXRpb24iLCJpYXQiOjE3NjYzODEyNjMsImV4cCI6MTc2NjQ2NzY2M30.ODSSeKFydOGsdK_uh-jmlF37I2vbNBMKmVcdRjtgxIs"

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
