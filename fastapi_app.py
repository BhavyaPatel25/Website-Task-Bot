from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.env import load_environment
from chains.task_classifier import build_task_classifier_chain
from chains.transformer_chain import build_transformer_chain
from tools.web_loader import load_web_page
from tools.content_extractor import extract_content
from models.schemas import TaskRequest, TaskResponse

# ---------- Environment ----------
load_environment()

# ---------- FastAPI App ----------
app = FastAPI(
    title="Web Task Agent API",
    description="API for automating website tasks like extraction, transformation, and summarization",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Web Task Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "process_task": "/process-task"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


@app.post("/process-task", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    """
    Process a web task based on URL and task description.
    
    Args:
        request: TaskRequest containing URL and task description
        
    Returns:
        TaskResponse with the processed content
        
    Raises:
        HTTPException: If processing fails
    """
    if not request.url or not request.task_description:
        raise HTTPException(
            status_code=400,
            detail="Both URL and task description are required"
        )
    
    try:
        # Step 1: Classify task intent
        task_chain = build_task_classifier_chain()
        intent = task_chain.invoke({
            "task_description": request.task_description
        })
        
        # Step 2: Fetch web page
        html = load_web_page.invoke({
            "url": request.url
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
        
        # Build response
        return TaskResponse(
            task_type=intent.task_type,
            output_format=intent.output_format,
            scope=intent.scope,
            content=transformed.content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the task: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
