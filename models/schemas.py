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
