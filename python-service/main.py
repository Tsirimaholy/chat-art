"""
Main entry point for FAQ Finance Chatbot (backward compatibility)

This module serves as a backward-compatible entry point for the refactored
FAQ Finance Chatbot service. It imports and runs the modular application.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    from app.core.logging import get_logger
    
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.service_name} on {settings.host}:{settings.port}")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )