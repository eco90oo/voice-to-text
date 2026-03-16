"""
Pydantic models for transcription API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TranscriptionRequest(BaseModel):
    """Request model for audio transcription."""
    
    language: Optional[str] = Field(
        default=None,
        description="Language of the audio (e.g., 'en', 'zh', 'ja'). If None, auto-detect."
    )
    prompt: Optional[str] = Field(
        default=None,
        description="Optional prompt to guide the model's style or correct terminology."
    )
    response_format: str = Field(
        default="json",
        description="Format of the response: 'json', 'text', 'srt', 'vtt', or 'verbose_json'."
    )
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Sampling temperature between 0 and 1."
    )


class TranscriptionResponse(BaseModel):
    """Response model for successful transcription."""
    
    text: str = Field(description="Transcribed text")
    language: str = Field(description="Detected or specified language")
    duration: Optional[float] = Field(default=None, description="Audio duration in seconds")
    model: str = Field(description="Model used for transcription")


class ErrorResponse(BaseModel):
    """Standardized error response."""
    
    code: str = Field(description="Error code")
    message: str = Field(description="Error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")
