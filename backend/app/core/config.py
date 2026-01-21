"""Configuration management for the application.
Uses pydantic-settings for environment variable management.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator
from typing import Optional, Union
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Mapey Roadmap API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS Settings - can be comma-separated string or list
    CORS_ORIGINS: Union[str, list[str]] = "http://localhost:3000,http://localhost:3001"
    
    # LLM Settings - Gemini via LangChain
    GEMINI_API_KEY: Optional[str] = None
    # Optional: support GOOGLE_API_KEY as an alternative env var name
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3-pro-preview"
    GEMINI_TEMPERATURE: float = 0.4
    
    # Tavily API
    TAVILY_API_KEY: Optional[str] = None
    
    # Embedding Model
    EMBED_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # 'json' or 'text'
    
    # Vector Store
    VECTOR_STORE_INDEX_PATH: Optional[str] = None  # Optional: persist index to disk
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Union[str, list[str]] = ".pdf,.txt,.docx"

    # Backend JWT auth
    BACKEND_JWT_SECRET: str = "change-me"

    @model_validator(mode="after")
    def set_gemini_from_google(self):
        """Allow using GOOGLE_API_KEY as fallback for GEMINI_API_KEY."""
        if not self.GEMINI_API_KEY and self.GOOGLE_API_KEY:
            object.__setattr__(self, "GEMINI_API_KEY", self.GOOGLE_API_KEY)
        return self
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins string into list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        """Parse comma-separated extensions string into list."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Ignore any extra environment variables (e.g. legacy OLLAMA_* keys)
        extra = "ignore"


settings = Settings()
