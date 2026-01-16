# Website-Task-Bot

A Python bot that automates common website tasks — for example: extracting content, transforming formats, summarizing pages, or performing content analysis.

## Why this project exists
- Save time by automating repetitive website tasks
- Provide a simple, extensible Python codebase to add new automated jobs
- Available as both a Streamlit UI and FastAPI REST API

## Main features
- Task automation for website-related workflows
- AI-powered task classification and content transformation
- Multiple output formats: text, HTML, markdown, JSON
- Configurable via environment variables
- Available as web UI (Streamlit) or REST API (FastAPI)

## Quick start

### 1. Clone the repo
```bash
git clone https://github.com/BhavyaPatel25/Website-Task-Bot.git
cd Website-Task-Bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the application

#### Option A: Streamlit UI (Original)
```bash
streamlit run app.py
```
Then open your browser to http://localhost:8501

#### Option B: FastAPI REST API (New)
```bash
python fastapi_app.py
```
Or with uvicorn directly:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Process a Task
```bash
curl -X POST "http://localhost:8000/process-task" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "task_description": "Extract all text and convert it into clean HTML sections"
  }'
```

### Example with Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/process-task",
    json={
        "url": "https://example.com",
        "task_description": "Summarize the main content in markdown format"
    }
)

result = response.json()
print(result["content"])
```

## Want to help or ask a question?
- Repository: https://github.com/BhavyaPatel25/Website-Task-Bot
- Open an issue or submit a pull request with improvements
