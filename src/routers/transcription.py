"""
API routers for transcription endpoints.
"""
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from ..schemas import TranscriptionRequest, TranscriptionResponse, ErrorResponse
from ..services import TranscriptionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/transcription", tags=["transcription"])


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    language: str = None,
    prompt: str = None,
    response_format: str = "json",
    temperature: float = 0.0,
) -> TranscriptionResponse:
    """
    Transcribe audio file to text using OpenAI Whisper API.

    Supported audio formats: mp3, mp4, m4a, wav, webm, flac

    Args:
        file: Audio file upload
        language: Language code (optional, auto-detect if not provided)
        prompt: Optional prompt to guide transcription
        response_format: Output format (json, text, srt, vtt, verbose_json)
        temperature: Sampling temperature (0.0 to 1.0)

    Returns:
        TranscriptionResponse with transcribed text
    """
    logger.info(f"Received transcription request: {file.filename}")

    # Validate file
    if file.size is not None and file.size > 25 * 1024 * 1024:  # 25MB limit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 25MB limit",
        )

    # Create request object
    request = TranscriptionRequest(
        language=language,
        prompt=prompt,
        response_format=response_format,
        temperature=temperature,
    )

    # Get service and process
    service = TranscriptionService()

    try:
        # Read file content
        content = await file.read()
        from io import BytesIO
        audio_buffer = BytesIO(content)

        # Transcribe
        result = await service.transcribe_audio(
            audio_file=audio_buffer,
            filename=file.filename,
            request=request,
        )

        logger.info(f"Transcription completed: {len(result.text)} characters")
        return result

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service not properly configured",
        )
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}",
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "voice-to-text"}
