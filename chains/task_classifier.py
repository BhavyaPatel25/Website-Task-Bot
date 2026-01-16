from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from models.schemas import TaskIntent

from utils.env import load_environment
load_environment()

def build_task_classifier_chain():
    """
    Returns a LangChain runnable that converts a natural language task
    into a structured TaskIntent object.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.25
    )

    parser = PydanticOutputParser(
        pydantic_object=TaskIntent
    )

    prompt = PromptTemplate(
        template="""
            You are a task classification engine.

            Your job is to analyze the user's task description
            and convert it into a structured intent.

            Rules:
            - Output must strictly follow the JSON schema
            - Do NOT add explanations
            - Choose the closest matching intent
            - If unsure, prefer "extract_transform"

            {format_instructions}

            User task:
            {task_description}
        """,
        input_variables=["task_description"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | llm | parser
    return chain
