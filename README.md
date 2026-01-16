# Website-Task-Bot

A Python-based web task automation agent that extracts, transforms, and processes content from websites using AI. Available as both a Streamlit UI and a FastAPI service.

## Why this project exists
- Save time by automating repetitive website tasks
- Provide a simple, extensible Python codebase to add new automated jobs
- Leverage AI to intelligently process and transform web content

## Main features
- Task automation for website-related workflows (extract, transform, summarize)
- AI-powered content classification and transformation
- Multiple output formats: text, HTML, markdown, JSON
- Available as both web UI (Streamlit) and REST API (FastAPI)
- Configurable via environment variables

## Quick start

### Prerequisites
1. Clone the repo:
   ```bash
   git clone https://github.com/BhavyaPatel25/Website-Task-Bot.git
   cd Website-Task-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Streamlit UI
Run the web interface:
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Running the FastAPI Service
Start the API server:
```bash
python fastapi_app.py
```
Or using uvicorn directly:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

#### API Documentation
Once running, access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

#### API Endpoints

**POST /process-task**
Process a web task with the following JSON payload:
```json
{
  "url": "https://example.com",
  "task_description": "Extract all text and convert it into clean HTML sections"
}
```

Response:
```json
{
  "task_type": "extract_transform",
  "output_format": "html",
  "scope": "main_content",
  "content": "<section>...</section>",
  "success": true
}
```

**GET /health**
Health check endpoint returning system status.

#### Example cURL Request
```bash
curl -X POST "http://localhost:8000/process-task" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "task_description": "Summarize the main content in markdown format"
  }'
```

## Deployment

### Production Deployment
For production deployment, use a production ASGI server:

```bash
# Install gunicorn with uvicorn worker
pip install gunicorn

# Run with gunicorn
gunicorn fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t website-task-bot .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key website-task-bot
```

## Want to help or ask a question?
- Repository: https://github.com/BhavyaPatel25/Website-Task-Bot
- Open an issue or submit a pull request with improvements
