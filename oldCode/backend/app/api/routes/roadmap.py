"""
API routes for roadmap generation.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from typing import Optional
from app.models.schemas import RoadmapRequest, RoadmapResponse, ErrorResponse
from app.services.agents import roadmap_graph, MapeyState
from app.services.file_processor import read_resume_file, chunk_text
from app.services.vector_store import get_vector_store
from app.core.config import settings
from app.core.auth import get_current_user
from app.core.logging import get_logger
import time

logger = get_logger(__name__)

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.post("/generate", response_model=RoadmapResponse)
async def generate_roadmap(
    current_user: dict = Depends(get_current_user),
    topic: str = Form(...),
    resume_file: UploadFile = File(...),
    jd: Optional[str] = Form(None)
):
    """
    Generate a career roadmap based on resume, target role, and optional job description.
    
    Args:
        topic: Target career role or path
        resume_file: Uploaded resume file (PDF or TXT)
        jd: Optional job description text
        
    Returns:
        Complete roadmap with analysis, skill gaps, curriculum, and resources
    """
    request_id = f"req_{int(time.time() * 1000)}"
    start_time = time.time()
    
    logger.info(
        f"Roadmap generation request received",
        extra={
            "request_id": request_id,
            "topic": topic,
            "resume_filename": resume_file.filename,
            "has_jd": jd is not None
        }
    )
    
    try:
        # Validate file
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = "." + resume_file.filename.split(".")[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Read and validate file size
        file_content = await resume_file.read()
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )
        
        # Process resume file
        logger.info(f"Processing resume file: {resume_file.filename}")
        resume_text = read_resume_file(file_content, resume_file.filename)
        
        if len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume appears to be empty or unreadable. Please ensure the file contains text."
            )
        
        # Add resume to vector store for RAG
        chunks = chunk_text(resume_text)
        vector_store = get_vector_store()
        vector_store.add_texts(chunks)
        logger.info(f"Added {len(chunks)} resume chunks to vector store")
        
        # Prepare state for LangGraph
        initial_state: MapeyState = {
            "topic": topic.strip(),
            "resume": resume_text,
            "jd": jd or "",
            "analysis": "",
            "skill_gaps": "",
            "curriculum": "",
            "rag_context": "",
            "resources": "",
            "roadmap": ""
        }
        
        # Execute the roadmap generation graph
        logger.info(f"Starting roadmap generation workflow")
        result = roadmap_graph.invoke(initial_state)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(
            f"Roadmap generation completed successfully",
            extra={
                "request_id": request_id,
                "processing_time_seconds": round(processing_time, 2)
            }
        )
        
        # Return response
        response = RoadmapResponse(
            roadmap=result.get("roadmap", ""),
            skill_gaps=result.get("skill_gaps", ""),
            curriculum=result.get("curriculum", ""),
            resources=result.get("resources", ""),
            analysis=result.get("analysis"),
            rag_context=result.get("rag_context")
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error generating roadmap: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/generate-from-text", response_model=RoadmapResponse)
async def generate_roadmap_from_text(
    request: RoadmapRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a career roadmap from text input (no file upload).
    Useful for API integrations.
    
    Args:
        request: RoadmapRequest with topic, resume text, and optional JD
        
    Returns:
        Complete roadmap with analysis, skill gaps, curriculum, and resources
    """
    request_id = f"req_{int(time.time() * 1000)}"
    start_time = time.time()
    
    logger.info(
        f"Roadmap generation from text request received",
        extra={
            "request_id": request_id,
            "topic": request.topic,
            "resume_length": len(request.resume),
            "has_jd": request.jd is not None
        }
    )
    
    try:
        # Add resume to vector store for RAG
        chunks = chunk_text(request.resume)
        vector_store = get_vector_store()
        vector_store.add_texts(chunks)
        logger.info(f"Added {len(chunks)} resume chunks to vector store")
        
        # Prepare state for LangGraph
        initial_state: MapeyState = {
            "topic": request.topic,
            "resume": request.resume,
            "jd": request.jd or "",
            "analysis": "",
            "skill_gaps": "",
            "curriculum": "",
            "rag_context": "",
            "resources": "",
            "roadmap": ""
        }
        
        # Execute the roadmap generation graph
        logger.info(f"Starting roadmap generation workflow")
        result = roadmap_graph.invoke(initial_state)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(
            f"Roadmap generation completed successfully",
            extra={
                "request_id": request_id,
                "processing_time_seconds": round(processing_time, 2)
            }
        )
        
        # Return response
        response = RoadmapResponse(
            roadmap=result.get("roadmap", ""),
            skill_gaps=result.get("skill_gaps", ""),
            curriculum=result.get("curriculum", ""),
            resources=result.get("resources", ""),
            analysis=result.get("analysis"),
            rag_context=result.get("rag_context")
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Error generating roadmap: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/vector-store/stats")
async def get_vector_store_stats():
    """Get statistics about the vector store."""
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting vector store stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vector-store/clear")
async def clear_vector_store():
    """Clear all data from the vector store."""
    try:
        vector_store = get_vector_store()
        vector_store.clear()
        logger.info("Vector store cleared via API")
        return {"message": "Vector store cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing vector store: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
