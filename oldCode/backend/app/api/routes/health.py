"""
Health check and status endpoints.
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Add any health checks here (database, external services, etc.)
        return HealthResponse(
            status="healthy",
            version=settings.VERSION,
            service=settings.PROJECT_NAME
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return HealthResponse(
            status="unhealthy",
            version=settings.VERSION,
            service=settings.PROJECT_NAME
        )
