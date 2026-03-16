"""
Repository layer for Whisper API interaction.
"""
import openai
import logging
from typing import BinaryIO, Optional
from io import BytesIO

from ..config import settings

logger = logging.getLogger(__name__)


class WhisperRepository:
    """Repository for interacting with OpenAI Whisper API."""

    def __init__(self) -> None:
        """Initialize the repository with OpenAI client."""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_whisper_model
        logger.info(f"WhisperRepository initialized with model: {self.model}")

    async def transcribe(
        self,
        audio_file: BinaryIO,
        filename: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: str = "json",
        temperature: float = 0.0,
    ) -> dict:
        """
        Transcribe audio file using Whisper API.

        Args:
            audio_file: Binary audio file object
            filename: Name of the audio file (e.g., 'audio.mp3')
            language: Language code (optional, auto-detect if None)
            prompt: Optional prompt for the model
            response_format: Output format (json, text, srt, vtt, verbose_json)
            temperature: Sampling temperature (0-1)

        Returns:
            Dictionary containing transcription results
        """
        logger.info(f"Starting transcription for file: {filename}")

        # Reset file pointer to beginning
        audio_file.seek(0)

        try:
            response = await openai.audio.transcriptions.create(
                model=self.model,
                file=(filename, audio_file),
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature,
            )

            result = {
                "text": response.text if hasattr(response, "text") else str(response),
                "language": language or "auto-detected",
                "model": self.model,
            }

            # Add duration if available in verbose_json format
            if hasattr(response, "duration"):
                result["duration"] = response.duration

            logger.info(f"Transcription completed successfully for: {filename}")
            return result

        except openai.APIError as e:
            logger.error(f"OpenAI API error during transcription: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during transcription: {str(e)}")
            raise
