"""
Vector store service using FAISS for RAG operations with Ollama embeddings.
"""
import faiss
import numpy as np
from typing import List, Optional
from app.core.config import settings
from app.core.logging import get_logger
import pickle
from pathlib import Path
from ollama import Client

logger = get_logger(__name__)


class VectorStore:
    """FAISS-based vector store for semantic search using Ollama embeddings."""
    
    def __init__(self):
        self.index: Optional[faiss.Index] = None
        self.texts: List[str] = []
        self.ollama_client: Optional[Client] = None
        self._initialize_model()
        
        # Load persisted index if available
        if settings.VECTOR_STORE_INDEX_PATH:
            self._load_index()
    
    def _initialize_model(self, retry_count: int = 0, max_retries: int = 3):
        """Initialize the Ollama client for embeddings with retry logic."""
        import time
        
        try:
            ollama_url = settings.OLLAMA_BASE_URL
            logger.info(f"Connecting to Ollama at: {ollama_url} (attempt {retry_count + 1}/{max_retries + 1})")
            self.ollama_client = Client(host=ollama_url)
            
            # Test connection by getting embeddings for a simple test
            test_embedding = self.ollama_client.embeddings(
                model=settings.EMBED_MODEL_NAME,
                prompt="test"
            )
            logger.info(f"Successfully initialized VectorStore with Ollama embeddings model: {settings.EMBED_MODEL_NAME} (dim: {len(test_embedding['embedding'])})")
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama client (attempt {retry_count + 1}/{max_retries + 1}): {str(e)}")
            
            if retry_count < max_retries:
                # Wait before retrying (exponential backoff)
                wait_time = 2 ** retry_count
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return self._initialize_model(retry_count + 1, max_retries)
            else:
                logger.error(f"Failed to initialize Ollama client after {max_retries + 1} attempts", exc_info=True)
                logger.warning("Vector store will not be available. Make sure Ollama is running.")
                # Don't raise - allow service to start without vector store
                self.ollama_client = None
    
    def _ensure_initialized(self):
        """Retry initialization if client is missing."""
        if self.ollama_client is None:
            logger.info("Ollama client not initialized, attempting to reconnect...")
            self._initialize_model()

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
        
        self._ensure_initialized()
        if self.ollama_client is None:
            raise RuntimeError("Ollama client not initialized. Cannot add texts.")
        
        try:
            # Get embeddings from Ollama for each text
            embeddings = []
            for text in texts:
                response = self.ollama_client.embeddings(
                    model=settings.EMBED_MODEL_NAME,
                    prompt=text
                )
                embeddings.append(response['embedding'])
            
            embeds = np.array(embeddings, dtype='float32')
            dim = embeds.shape[1]
            
            if self.index is None:
                self.index = faiss.IndexFlatL2(dim)
                logger.info(f"Created new FAISS index with dimension: {dim}")
            
            self.index.add(embeds)
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
        
        self._ensure_initialized()
        if self.ollama_client is None:
            logger.error("Ollama client not initialized. Cannot search.")
            return []
        
        try:
            # Get query embedding from Ollama
            response = self.ollama_client.embeddings(
                model=settings.EMBED_MODEL_NAME,
                prompt=query
            )
            q_emb = np.array([response['embedding']], dtype='float32')
            
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
