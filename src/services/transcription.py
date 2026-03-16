"""
Service layer for transcription business logic.
"""
import logging
from typing import BinaryIO, Optional

from ..repositories import WhisperRepository
from ..schemas import TranscriptionRequest, TranscriptionResponse

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for handling transcription business logic."""

    def __init__(self) -> None:
        """Initialize the service with repository dependency."""
        self.repository = WhisperRepository()
        logger.info("TranscriptionService initialized")

    async def transcribe_audio(
        self,
        audio_file: BinaryIO,
        filename: str,
        request: TranscriptionRequest,
    ) -> TranscriptionResponse:
        """
        Transcribe audio file with business logic validation.

        Args:
            audio_file: Binary audio file
            filename: Name of the audio file
            request: Transcription request parameters

        Returns:
            TranscriptionResponse with transcribed text
        """
        logger.info(f"Processing transcription request for: {filename}")

        # Validate audio file format
        valid_extensions = ["mp3", "mp4", "m4a", "wav", "webm", "flac"]
        ext = filename.split(".")[-1].lower()
        
        if ext not in valid_extensions:
            logger.warning(f"Unsupported audio format: {ext}")

        # Call repository
        result = await self.repository.transcribe(
            audio_file=audio_file,
            filename=filename,
            language=request.language,
            prompt=request.prompt,
            response_format=request.response_format,
            temperature=request.temperature,
        )

        # Return structured response
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            duration=result.get("duration"),
            model=result["model"],
        )
