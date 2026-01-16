from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from models.schemas import TaskIntent

from utils.env import load_environment
load_environment()

def build_transformer_chain(intent: TaskIntent):
    """
    Builds a transformation chain based on task intent.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.25
    )

    if intent.output_format == "html":
        format_instructions = """
            Convert the content into clean, semantic HTML.
            Rules:
            - Use <section>, <h1>-<h3>, <p>, <ul>, <li>
            - Do NOT include <html>, <head>, or <body>
            - No inline CSS or JavaScript
            - Preserve logical structure
        """
    elif intent.output_format == "markdown":
        format_instructions = """
            Convert the content into clean Markdown.
            Rules:
            - Use #, ##, ### for headings
            - Use bullet points where appropriate
            - No code fences unless necessary
        """
    elif intent.output_format == "json":
        format_instructions = """
            Convert the content into structured JSON.
            Rules:
            - Keys must be semantic
            - Values must be strings or arrays
            - Output must be valid JSON only
        """
    else:
        format_instructions = """
            Clean and normalize the text.
            Rules:
            - Remove redundancy
            - Preserve paragraphs
        """

    prompt = PromptTemplate(
        template="""
            You are a content transformation engine.

            Task:
            Transform the provided content according to the rules below.

            {format_instructions}

            Content:
            {content}
        """,
        input_variables=["content"],
        partial_variables={
            "format_instructions": format_instructions
        }
    )

    chain = prompt | llm
    return chain
