# Voice-to-Text API

Speech-to-text transcription service using OpenAI Whisper API.

## Features

- FastAPI-based REST API
- OpenAI Whisper API integration
- Clean Architecture (routers, services, repositories)
- Type-safe with Pydantic
- Environment-based configuration

## Setup

### 1. Create virtual environment and install dependencies

```bash
cd voice-to-text
uv venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

uv pip install -e .
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
python -m src.main
```

## API Endpoints

### POST /api/v1/transcription/transcribe

Transcribe audio file to text.

**Request:**
- `file`: Audio file (multipart/form-data)
- `language`: Language code (optional, e.g., 'en', 'zh')
- `prompt`: Optional prompt for the model
- `response_format`: Output format (json, text, srt, vtt, verbose_json)
- `temperature`: Sampling temperature (0.0 to 1.0)

**Response:**
```json
{
  "text": "Transcribed text here",
  "language": "en",
  "duration": 120.5,
  "model": "whisper-1"
}
```

### GET /api/v1/transcription/health

Health check endpoint.

### GET /

Root endpoint.

## Supported Audio Formats

- mp3
- mp4
- m4a
- wav
- webm
- flac

## License

MIT
