from pydantic import BaseModel, Field
from typing import Literal


class TaskIntent(BaseModel):
    task_type: Literal[
        "extract",
        "transform",
        "extract_transform",
        "summarize",
        "qa"
    ] = Field(
        description="High-level task category"
    )

    output_format: Literal[
        "text",
        "html",
        "markdown",
        "json"
    ] = Field(
        description="Desired output format"
    )

    scope: Literal[
        "full_page",
        "main_content",
        "headings_only"
    ] = Field(
        description="Scope of content to operate on"
    )


class TaskRequest(BaseModel):
    url: str = Field(
        description="The target URL to process",
        examples=["https://example.com"]
    )
    task_description: str = Field(
        description="Description of the task to perform",
        examples=["Extract all text and convert it into clean HTML sections"]
    )


class TaskResponse(BaseModel):
    task_type: str = Field(
        description="The classified task type"
    )
    output_format: str = Field(
        description="The output format used"
    )
    scope: str = Field(
        description="The scope of content processed"
    )
    content: str = Field(
        description="The transformed content"
    )
