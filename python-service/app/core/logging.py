"""
Logging utilities for FAQ Finance Chatbot

This module contains logging configuration and utility functions
for consistent logging throughout the application.
"""

import logging
import sys
from datetime import datetime
from typing import List

from .config import settings


def setup_logging() -> None:
    """
    Configure application logging with consistent format
    """
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name (str): Logger name, typically __name__
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


def log_interaction(question: str, answer: str, sources: List[str], similarity_score: float = None) -> None:
    """
    Log chat interactions with detailed information
    
    Args:
        question (str): User's question
        answer (str): Bot's response
        sources (List[str]): Source IDs used for the answer
        similarity_score (float, optional): Matching score for debugging
    """
    timestamp = datetime.now().isoformat()
    
    # Console output for development
    print(f"\n{'=' * 60}")
    print(f"[{timestamp}]")
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Sources: {', '.join(sources) if sources else 'None (fallback response)'}")
    if similarity_score is not None:
        print(f"Similarity Score: {similarity_score:.3f}")
    print(f"{'=' * 60}\n")
    
    # Structured logging for production
    logger = get_logger("faq_chatbot.interaction")
    logger.info(
        "Chat interaction",
        extra={
            "timestamp": timestamp,
            "question": question,
            "answer_length": len(answer),
            "sources": sources,
            "similarity_score": similarity_score,
            "has_match": len(sources) > 0
        }
    )


def log_matching_debug(query: str, similarity_score: float) -> None:
    """
    Log matching process details for debugging
    
    Args:
        query (str): User's query
        similarity_score (float): Best matching score
    """
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Query: '{query}' | Best match score: {similarity_score:.3f}")
    
    logger = get_logger("faq_chatbot.matching")
    logger.debug(
        "Question matching",
        extra={
            "query": query,
            "similarity_score": similarity_score,
            "threshold": settings.similarity_threshold
        }
    )