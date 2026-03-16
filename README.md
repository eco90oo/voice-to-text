# Voice-to-Text API

Speech-to-text transcription service using OpenAI Whisper API.

## Features

- FastAPI-based REST API
- OpenAI Whisper API integration
- Clean Architecture (routers, services, repositories)
- Type-safe with Pydantic
- Environment-based configuration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (package manager)

---

## 📋 Installation Steps

### Step 1: Clone the repository

```bash
git clone https://github.com/eco90oo/voice-to-text.git
cd voice-to-text
```

### Step 2: Create virtual environment and install dependencies

```bash
# Create virtual environment using uv
uv venv

# Activate virtual environment
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

### Step 3: Configure environment variables

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Open `.env` and fill in your OpenAI API Key:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_actual_openai_api_key_here
OPENAI_WHISPER_MODEL=whisper-1

# Application Settings
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO
```

> **Note:** Get your OpenAI API key from: https://platform.openai.com/api-keys

---

## ▶️ Run the Server

### Option 1: Using uvicorn (recommended)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Run directly

```bash
python -m src.main
```

---

## 🔗 API Endpoints

Once the server is running, visit:

- **Swagger UI (Interactive API Docs)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/api/v1/transcription/health

---

## 📤 Usage Example

### Transcribe Audio

**Endpoint:** `POST /api/v1/transcription/transcribe`

**Using curl:**

```bash
curl -X POST "http://localhost:8000/api/v1/transcription/transcribe" \
  -F "file=@your_audio_file.mp3" \
  -F "language=en" \
  -F "temperature=0.0"
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | Audio file (mp3, mp4, m4a, wav, webm, flac) |
| `language` | string | No | Language code (e.g., 'en', 'zh', 'ja'). Auto-detect if not provided |
| `prompt` | string | No | Optional prompt to guide transcription |
| `response_format` | string | No | Output format: json, text, srt, vtt, verbose_json (default: json) |
| `temperature` | float | No | Sampling temperature 0.0-1.0 (default: 0.0) |

**Response:**

```json
{
  "text": "Transcribed text here",
  "language": "en",
  "duration": 120.5,
  "model": "whisper-1"
}
```

---

## ⚠️ Troubleshooting

### "OPENAI_API_KEY is not set"

Make sure you have created `.env` file with your OpenAI API key. The key must be a valid OpenAI API key with access to Whisper API.

### "File size exceeds 25MB limit"

Maximum file size is 25MB. Split longer audio files if needed.

### Port 8000 is already in use

Use a different port:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

---

## 📁 Project Structure

```
voice-to-text/
├── .env                    # API Key 設定（不要提交到 Git）
├── .env.example            # 環境變數範本
├── .gitignore
├── pyproject.toml          # uv 依賴管理
├── README.md               # 本文件
└── src/
    ├── config.py           # pydantic-settings 配置
    ├── main.py             # FastAPI 入口
    ├── schemas/
    │   └── transcription.py # Pydantic models
    ├── services/
    │   └── transcription.py # 商業邏輯
    ├── repositories/
    │   └── whisper.py       # Whisper API 互動
    └── routers/
        └── transcription.py # API 端點
```

---

## 🧪 Testing

Install dev dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

---

## 📄 License

MIT

---

## 👤 Author

eco90oo / OpenClaw AI Assistant
