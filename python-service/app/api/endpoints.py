"""
API endpoints for FAQ Finance Chatbot

This module contains all API route handlers for the FAQ Finance Chatbot service.
It defines the REST endpoints and their business logic.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..models.schemas import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    ServiceInfoResponse
)
from ..services.faq_service import faq_service, FAQServiceError
from ..core.logging import log_interaction, get_logger
from ..core.config import settings

logger = get_logger(__name__)

# Create API router
router = APIRouter()


async def get_faq_service():
    """
    Dependency to get initialized FAQ service
    
    Returns:
        FAQService: Initialized FAQ service instance
    
    Raises:
        HTTPException: If service initialization fails
    """
    try:
        if not faq_service._initialized:
            faq_service.initialize()
        return faq_service
    except FAQServiceError as e:
        logger.error(f"FAQ service initialization failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Service initialization failed: {str(e)}"
        )


@router.get("/", response_model=ServiceInfoResponse)
async def get_service_info():
    """
    Get service information
    
    Returns basic information about the FAQ Finance Chatbot service
    including available endpoints and current status.
    """
    return ServiceInfoResponse(
        service=settings.service_name,
        status="running",
        endpoints=["/chat", "/health"]
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service = Depends(get_faq_service)
):
    """
    Process a chat message and return an answer
    
    This endpoint accepts a user question and returns the most appropriate
    answer from the FAQ knowledge base. If no suitable answer is found,
    it returns a fallback response.
    
    Args:
        request (ChatRequest): User's chat message
        service: Injected FAQ service dependency
    
    Returns:
        ChatResponse: Bot's response with answer and sources
    
    Raises:
        HTTPException: If request processing fails
    """
    query = request.message.strip()
    
    if not query:
        raise HTTPException(
            status_code=400, 
            detail="Message cannot be empty"
        )
    
    try:
        # Process the query using the FAQ service
        result = service.process_query(query)
        
        # Extract response data
        answer = result['answer']
        sources = result['sources']
        similarity_score = result.get('similarity_score')
        
        # Log the interaction
        log_interaction(query, answer, sources, similarity_score)
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except FAQServiceError as e:
        logger.error(f"FAQ service error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your question. Please try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )


@router.get("/health", response_model=HealthResponse)
async def health_check(service = Depends(get_faq_service)):
    """
    Health check endpoint
    
    Returns the current health status of the service including
    the number of FAQ entries loaded and overall service status.
    
    Args:
        service: Injected FAQ service dependency
    
    Returns:
        HealthResponse: Service health status and statistics
    """
    try:
        stats = service.get_service_stats()
        
        return HealthResponse(
            status="healthy",
            faq_entries=stats.get('total_entries', 0)
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service unhealthy"
        )


@router.get("/stats")
async def get_service_stats(service = Depends(get_faq_service)):
    """
    Get detailed service statistics
    
    This endpoint provides detailed information about the service
    including knowledge base statistics, matching configuration,
    and service status. Useful for monitoring and debugging.
    
    Args:
        service: Injected FAQ service dependency
    
    Returns:
        dict: Detailed service statistics
    """
    try:
        stats = service.get_service_stats()
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"Failed to get service stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve service statistics"
        )


@router.post("/search")
async def search_faq(
    request: ChatRequest,
    service = Depends(get_faq_service)
):
    """
    Search for multiple matching FAQ entries
    
    This endpoint returns multiple potential matches for a query,
    useful for showing alternative answers or debugging matching logic.
    
    Args:
        request (ChatRequest): Search query
        service: Injected FAQ service dependency
    
    Returns:
        dict: Multiple matching FAQ entries with similarity scores
    """
    query = request.message.strip()
    
    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )
    
    try:
        matches = service.get_multiple_matches(query, top_k=5)
        
        return JSONResponse(content={
            "query": query,
            "matches": [
                {
                    "id": match["id"],
                    "question": match["q"],
                    "answer": match["a"],
                    "similarity_score": match.get("_similarity_score", 0.0)
                }
                for match in matches
            ],
            "total_matches": len(matches)
        })
        
    except FAQServiceError as e:
        logger.error(f"FAQ service error during search: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to search FAQ entries"
        )
    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during search"
        )