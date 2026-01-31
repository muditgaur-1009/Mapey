"""
File processing utilities for resume parsing.
"""
from typing import BinaryIO
from pypdf import PdfReader
from app.core.config import settings
from app.core.logging import get_logger
import io

logger = get_logger(__name__)


def read_resume_file(file_content: bytes, filename: str) -> str:
    """
    Read and extract text from resume file.
    
    Args:
        file_content: Binary file content
        filename: Original filename with extension
        
    Returns:
        Extracted text content
    """
    try:
        if filename.lower().endswith(".pdf"):
            file_obj = io.BytesIO(file_content)
            reader = PdfReader(file_obj)
            text = "\n".join(
                page.extract_text() or "" 
                for page in reader.pages
            )
            logger.info(f"Successfully extracted text from PDF: {filename}, {len(text)} characters")
            return text
        elif filename.lower().endswith(".txt"):
            text = file_content.decode("utf-8", errors="ignore")
            logger.info(f"Successfully read text file: {filename}, {len(text)} characters")
            return text
        else:
            # Try to decode as text for other formats
            text = file_content.decode("utf-8", errors="ignore")
            logger.warning(f"Unknown file type for {filename}, attempting text decode")
            return text
    except Exception as e:
        logger.error(f"Error reading file {filename}: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to process file {filename}: {str(e)}")


def chunk_text(text: str, size: int = 500) -> list[str]:
    """
    Chunk text into smaller pieces for vector storage.
    
    Args:
        text: Input text to chunk
        size: Number of words per chunk
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = [" ".join(words[i:i+size]) for i in range(0, len(words), size)]
    logger.debug(f"Chunked text into {len(chunks)} chunks of ~{size} words each")
    return chunks
