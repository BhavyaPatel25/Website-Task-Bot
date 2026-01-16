from dotenv import load_dotenv
import os

def load_environment():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. "
            "Please define it in a .env file or environment variables."
        )
