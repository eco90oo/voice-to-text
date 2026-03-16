"""
Voice-to-Text API - Main Application Entry Point

A FastAPI-based speech-to-text service using OpenAI Whisper API.
"""
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import transcription_router
from .schemas import ErrorResponse


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    logger.info("Voice-to-Text API starting up...")
    logger.info(f"Log level: {settings.log_level}")
    
    yield
    
    logger.info("Voice-to-Text API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Voice-to-Text API",
    description="Speech-to-text transcription service using OpenAI Whisper API",
    version="1.0.0",
    lifespan=lifespan,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions with standardized error response."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            details={"path": str(request.url)},
        ).model_dump(),
    )


# Include routers
app.include_router(transcription_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Voice-to-Text API",
        "version": "1.0.0",
        "status": "running",
    }


# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
