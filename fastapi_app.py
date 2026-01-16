from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

from utils.env import load_environment
from chains.task_classifier import build_task_classifier_chain
from chains.transformer_chain import build_transformer_chain
from tools.web_loader import load_web_page
from tools.content_extractor import extract_content

# ---------- Environment ----------
load_environment()

# ---------- FastAPI App ----------
app = FastAPI(
    title="Web Task Agent API",
    description="API for automating website tasks: extract, transform, summarize content from web pages",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request/Response Models ----------
class TaskRequest(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="Target URL to process",
        json_schema_extra={"example": "https://example.com"}
    )
    task_description: str = Field(
        ...,
        description="Description of the task to perform",
        json_schema_extra={"example": "Extract all text and convert it into clean HTML sections"},
        min_length=1
    )

class TaskResponse(BaseModel):
    task_type: str = Field(
        description="The classified task type"
    )
    output_format: str = Field(
        description="The output format of the result"
    )
    scope: str = Field(
        description="The scope of content processed"
    )
    content: str = Field(
        description="The transformed content"
    )
    success: bool = Field(
        default=True,
        description="Whether the task completed successfully"
    )

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# ---------- API Endpoints ----------
@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint returning API status
    """
    return HealthResponse(
        status="online",
        message="Web Task Agent API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )

@app.post("/process-task", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    """
    Process a web task based on URL and task description.
    
    This endpoint:
    1. Classifies the task intent
    2. Fetches the web page
    3. Extracts readable content
    4. Transforms the content according to the task
    
    Returns the transformed content with metadata.
    """
    try:
        # Step 1: Classify task intent
        task_chain = build_task_classifier_chain()
        intent = task_chain.invoke({
            "task_description": request.task_description
        })
        
        # Step 2: Fetch web page
        html = load_web_page.invoke({
            "url": str(request.url)
        })
        
        # Step 3: Extract readable content
        extracted_text = extract_content.invoke({
            "html": html
        })
        
        # Step 4: Transform content
        transformer_chain = build_transformer_chain(intent)
        transformed = transformer_chain.invoke({
            "content": extracted_text
        })
        
        # Return response
        return TaskResponse(
            task_type=intent.task_type,
            output_format=intent.output_format,
            scope=intent.scope,
            content=transformed.content,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the task: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
