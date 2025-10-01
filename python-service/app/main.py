"""
Main application entry point for FAQ Finance Chatbot

This module creates and configures the FastAPI application with all
necessary middleware, routers, and startup/shutdown event handlers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.logging import setup_logging, get_logger
from .api.endpoints import router
from .services.faq_service import faq_service
from .services.knowledge_base import KnowledgeBaseError
from .services.faq_service import FAQServiceError

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    
    Handles startup and shutdown events for the FastAPI application.
    Initializes services during startup and performs cleanup during shutdown.
    """
    # Startup
    logger.info(f"Starting {settings.service_name} v{settings.service_version}")
    
    try:
        # Initialize FAQ service
        faq_service.initialize()
        logger.info("FAQ service initialized successfully")
        
        # Log service configuration
        logger.info(f"Service configured with threshold: {settings.similarity_threshold}")
        logger.info(f"CORS origins: {settings.cors_origins}")
        logger.info(f"FAQ data loaded from: {settings.faq_file_path}")
        
    except (KnowledgeBaseError, FAQServiceError) as e:
        logger.error(f"Failed to initialize services: {e}")
        # Don't exit completely, let health checks handle it
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.service_name}")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.service_name,
        description="A REST API service for answering finance-related questions using intelligent FAQ matching",
        version=settings.service_version,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Include API routes
    app.include_router(router)
    
    # Add global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler for unhandled errors"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )