"""
Vector store service using FAISS for RAG operations.
"""
import faiss
import numpy as np
from typing import List, Optional, TYPE_CHECKING
from app.core.config import settings
from app.core.logging import get_logger
import pickle
from pathlib import Path

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

logger = get_logger(__name__)


class VectorStore:
    """FAISS-based vector store for semantic search."""
    
    def __init__(self):
        self.index: Optional[faiss.Index] = None
        self.texts: List[str] = []
        self.embed_model: Optional["SentenceTransformer"] = None
        self._initialize_model()
        
        # Load persisted index if available
        if settings.VECTOR_STORE_INDEX_PATH:
            self._load_index()
    
    def _initialize_model(self):
        """Initialize the embedding model with error handling."""
        try:
            # Delay import to avoid startup errors if dependencies are missing
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading embedding model: {settings.EMBED_MODEL_NAME}")
            self.embed_model = SentenceTransformer(settings.EMBED_MODEL_NAME)
            logger.info(f"Successfully initialized VectorStore with model: {settings.EMBED_MODEL_NAME}")
        except ImportError as e:
            error_msg = (
                f"Failed to import required modules for SentenceTransformer.\n"
                f"Error: {str(e)}\n\n"
                f"Please install missing dependencies:\n"
                f"  pip install transformers torch sentence-transformers\n"
                f"Or run the fix script: fix_dependencies.bat (Windows) or fix_dependencies.sh (Linux/Mac)\n"
                f"See backend/INSTALLATION_TROUBLESHOOTING.md for detailed instructions."
            )
            logger.error(error_msg, exc_info=True)
            raise ImportError(error_msg) from e
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {str(e)}", exc_info=True)
            raise
    
    def add_texts(self, texts: List[str]) -> int:
        """
        Add texts to the vector store.
        
        Args:
            texts: List of text strings to embed and store
            
        Returns:
            Number of texts added
        """
        if not texts:
            logger.warning("Attempted to add empty text list to vector store")
            return 0
        
        if self.embed_model is None:
            raise RuntimeError("Embedding model not initialized. Cannot add texts.")
        
        try:
            embeds = self.embed_model.encode(texts, show_progress_bar=False)
            dim = embeds.shape[1]
            
            if self.index is None:
                self.index = faiss.IndexFlatL2(dim)
                logger.info(f"Created new FAISS index with dimension: {dim}")
            
            self.index.add(embeds.astype('float32'))
            self.texts.extend(texts)
            
            num_added = len(texts)
            logger.info(f"Added {num_added} texts to vector store. Total: {len(self.texts)}")
            
            # Persist index if path is configured
            if settings.VECTOR_STORE_INDEX_PATH:
                self._save_index()
            
            return num_added
        except Exception as e:
            logger.error(f"Error adding texts to vector store: {str(e)}", exc_info=True)
            raise
    
    def search(self, query: str, k: int = 4) -> List[str]:
        """
        Search for similar texts using semantic similarity.
        
        Args:
            query: Search query string
            k: Number of results to return
            
        Returns:
            List of most similar text chunks
        """
        if self.index is None or len(self.texts) == 0:
            logger.warning("Vector store is empty, returning empty results")
            return []
        
        if self.embed_model is None:
            logger.error("Embedding model not initialized. Cannot search.")
            return []
        
        try:
            q_emb = self.embed_model.encode([query], show_progress_bar=False)
            q_emb = q_emb.astype('float32')
            
            # Ensure k doesn't exceed available texts
            k = min(k, len(self.texts))
            
            D, I = self.index.search(q_emb, k)
            results = [self.texts[i] for i in I[0]]
            
            logger.debug(f"Search query: '{query[:50]}...', returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}", exc_info=True)
            return []
    
    def clear(self) -> None:
        """Clear all stored texts and reset the index."""
        self.index = None
        self.texts = []
        logger.info("Vector store cleared")
        
        # Remove persisted index file if it exists
        if settings.VECTOR_STORE_INDEX_PATH:
            index_path = Path(settings.VECTOR_STORE_INDEX_PATH)
            if index_path.exists():
                index_path.unlink()
                logger.info(f"Removed persisted index file: {index_path}")
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        return {
            "total_texts": len(self.texts),
            "index_created": self.index is not None,
            "dimension": self.index.d if self.index else None
        }
    
    def _save_index(self) -> None:
        """Save the index and texts to disk."""
        if not settings.VECTOR_STORE_INDEX_PATH or self.index is None:
            return
        
        try:
            index_path = Path(settings.VECTOR_STORE_INDEX_PATH)
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, str(index_path))
            
            # Save texts separately
            texts_path = index_path.with_suffix('.texts.pkl')
            with open(texts_path, 'wb') as f:
                pickle.dump(self.texts, f)
            
            logger.debug(f"Saved vector store index to {index_path}")
        except Exception as e:
            logger.warning(f"Failed to save vector store index: {str(e)}")
    
    def _load_index(self) -> None:
        """Load the index and texts from disk."""
        if not settings.VECTOR_STORE_INDEX_PATH:
            return
        
        try:
            index_path = Path(settings.VECTOR_STORE_INDEX_PATH)
            texts_path = index_path.with_suffix('.texts.pkl')
            
            if not index_path.exists() or not texts_path.exists():
                logger.info("No persisted index found, starting fresh")
                return
            
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load texts
            with open(texts_path, 'rb') as f:
                self.texts = pickle.load(f)
            
            logger.info(f"Loaded vector store index with {len(self.texts)} texts from {index_path}")
        except Exception as e:
            logger.warning(f"Failed to load vector store index: {str(e)}, starting fresh")


# Global vector store instance - lazy initialization
_vector_store_instance: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance (lazy initialization)."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance
