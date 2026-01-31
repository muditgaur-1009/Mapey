"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


class RoadmapRequest(BaseModel):
    """Request schema for roadmap generation."""
    topic: str = Field(..., min_length=1, max_length=200, description="Target role or career path")
    resume: str = Field(..., min_length=10, description="Resume content")
    jd: Optional[str] = Field(None, description="Job description (optional)")
    
    @field_validator("topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        return v.strip()


class RoadmapResponse(BaseModel):
    """Response schema for roadmap generation."""
    roadmap: str = Field(..., description="Generated career roadmap")
    skill_gaps: str = Field(..., description="Skill gap analysis")
    curriculum: str = Field(..., description="Learning curriculum plan")
    resources: str = Field(..., description="Learning resources and links")
    analysis: Optional[str] = Field(None, description="Role analysis")
    rag_context: Optional[str] = Field(None, description="RAG context used")


class HealthResponse(BaseModel):
    """Health check response."""
    status: Literal["healthy", "unhealthy"] = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    service: str = Field(..., description="Service name")


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code")
