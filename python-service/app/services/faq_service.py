"""
FAQ matching service for FAQ Finance Chatbot

This module contains the core business logic for matching user questions
with FAQ entries using TF-IDF vectorization and cosine similarity.
"""

from typing import Optional, Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from ..core.config import settings
from ..core.logging import get_logger, log_matching_debug
from .knowledge_base import KnowledgeBase, knowledge_base

logger = get_logger(__name__)


class FAQServiceError(Exception):
    """Custom exception for FAQ service related errors"""
    pass


class FAQService:
    """
    FAQ matching service using TF-IDF and cosine similarity
    
    This service handles the intelligent matching of user questions
    with the knowledge base using natural language processing techniques.
    """

    def __init__(self, kb: Optional[KnowledgeBase] = None, threshold: Optional[float] = None):
        """
        Initialize the FAQ service
        
        Args:
            kb (Optional[KnowledgeBase]): Knowledge base instance.
                                        If None, uses global instance.
            threshold (Optional[float]): Similarity threshold for matches.
                                       If None, uses settings default.
        """
        self.knowledge_base = kb or knowledge_base
        self.threshold = threshold or settings.similarity_threshold
        self._vectorizer = None
        self._faq_vectors = None
        self._initialized = False
    
    def initialize(self) -> None:
        """
        Initialize the TF-IDF vectorizer and FAQ vectors
        
        This method must be called before using the service.
        It prepares the vectorizer and computes vectors for all FAQ questions.
        
        Raises:
            FAQServiceError: If initialization fails
        """
        try:
            # Ensure knowledge base is loaded
            faq_questions = self.knowledge_base.questions
            
            if not faq_questions:
                raise FAQServiceError("No FAQ questions available for vectorization")
            
            # Initialize TF-IDF vectorizer
            self._vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words=None,  # Keep all words for better matching
                ngram_range=(1, 2),  # Use unigrams and bigrams
                max_features=5000  # Limit features for performance
            )
            
            # Fit and transform FAQ questions
            self._faq_vectors = self._vectorizer.fit_transform(faq_questions)
            self._initialized = True
            
            logger.info(f"FAQ service initialized with {len(faq_questions)} questions")
            logger.info(f"TF-IDF vocabulary size: {len(self._vectorizer.vocabulary_)}")
            
        except Exception as e:
            raise FAQServiceError(f"Failed to initialize FAQ service: {e}")
    
    def find_best_match(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Find the best matching FAQ entry for a user query
        
        Args:
            query (str): User's question
            
        Returns:
            Optional[Dict[str, Any]]: Best matching FAQ entry if similarity
                                    score exceeds threshold, None otherwise
        
        Raises:
            FAQServiceError: If service is not initialized or query processing fails
        """
        if not self._initialized:
            raise FAQServiceError("FAQ service not initialized. Call initialize() first.")
        
        if not query or not query.strip():
            return None
        
        try:
            # Transform the query using the fitted vectorizer
            query_vector = self._vectorizer.transform([query.strip()])
            
            # Calculate cosine similarity with all FAQ vectors
            similarities = cosine_similarity(query_vector, self._faq_vectors)[0]
            
            # Find the best match
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            # Log matching details for debugging
            log_matching_debug(query, best_score)
            
            # Check if score exceeds threshold
            if best_score > self.threshold:
                best_entry = self.knowledge_base.get_entry_by_index(best_idx)
                if best_entry:
                    # Add similarity score to the result for debugging
                    result = best_entry.copy()
                    result['_similarity_score'] = float(best_score)
                    return result
            
            return None
            
        except Exception as e:
            logger.error(f"Error during question matching: {e}")
            raise FAQServiceError(f"Failed to process query: {e}")
    
    def get_multiple_matches(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Get multiple matching FAQ entries for a query
        
        Args:
            query (str): User's question
            top_k (int): Number of top matches to return
            
        Returns:
            list[Dict[str, Any]]: List of top matching FAQ entries with scores
        """
        if not self._initialized:
            raise FAQServiceError("FAQ service not initialized. Call initialize() first.")
        
        if not query or not query.strip():
            return []
        
        try:
            query_vector = self._vectorizer.transform([query.strip()])
            similarities = cosine_similarity(query_vector, self._faq_vectors)[0]
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                score = similarities[idx]
                if score > self.threshold:
                    entry = self.knowledge_base.get_entry_by_index(int(idx))
                    if entry:
                        result = entry.copy()
                        result['_similarity_score'] = float(score)
                        results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error during multiple question matching: {e}")
            raise FAQServiceError(f"Failed to process query: {e}")
    
    def get_fallback_response(self) -> str:
        """
        Get the fallback response for when no suitable match is found
        
        Returns:
            str: Fallback response message
        """
        return (
            "Je suis désolé, je n'ai pas trouvé de réponse précise à votre question "
            "dans ma base de connaissances. Pourriez-vous reformuler ou poser une "
            "question sur l'EBITDA, les marges, le cash flow, ou d'autres "
            "indicateurs financiers ?"
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and return a complete response
        
        Args:
            query (str): User's question
            
        Returns:
            Dict[str, Any]: Response containing answer, sources, and metadata
        """
        # Find best match
        match = self.find_best_match(query)
        
        if match:
            return {
                'answer': match['a'],
                'sources': [match['id']],
                'similarity_score': match.get('_similarity_score'),
                'matched': True
            }
        else:
            return {
                'answer': self.get_fallback_response(),
                'sources': [],
                'similarity_score': 0.0,
                'matched': False
            }
    
    def get_service_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the FAQ service
        
        Returns:
            Dict[str, Any]: Service statistics
        """
        stats = {
            'initialized': self._initialized,
            'threshold': self.threshold,
            'vectorizer_vocab_size': len(self._vectorizer.vocabulary_) if self._vectorizer else 0,
            'faq_vectors_shape': self._faq_vectors.shape if self._faq_vectors is not None else None
        }
        
        # Add knowledge base stats
        stats.update(self.knowledge_base.get_stats())
        
        return stats
    
    def update_threshold(self, new_threshold: float) -> None:
        """
        Update the similarity threshold
        
        Args:
            new_threshold (float): New threshold value (0.0 to 1.0)
        """
        if not 0.0 <= new_threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        
        self.threshold = new_threshold
        logger.info(f"Updated similarity threshold to {new_threshold}")


# Global FAQ service instance
faq_service = FAQService()