import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev-secret"))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db"))
    cors_origins: list[str] = Field(
        default=os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:8080").split(",")
    )


settings = Settings()
