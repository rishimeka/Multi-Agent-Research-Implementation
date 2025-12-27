import dotenv
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm(temperature: float = 0) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI instance with the given temperature."""
    return ChatOpenAI(
            model="gpt-5-nano",
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

