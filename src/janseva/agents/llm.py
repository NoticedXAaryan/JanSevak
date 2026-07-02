"""
LLM provider factory.
Returns the configured LLM instance based on settings.
Supports Google Gemini (production) and Ollama (local development).
"""
from langchain_core.language_models import BaseChatModel
from janseva.config import settings


def get_llm() -> BaseChatModel:
    """
    Create and return the configured LLM instance.
    
    Uses LLM_PROVIDER from settings:
    - 'gemini': Google Gemini API (requires GOOGLE_API_KEY)
    - 'ollama': Local Ollama instance (requires Ollama running)
    """
    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # Low temperature for factual government info
            max_output_tokens=2048,
        )
    elif settings.llm_provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        
        return ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0.3,
        )
    elif settings.llm_provider == "openrouter":
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.3,
            max_tokens=2048,
        )
    else:
        raise ValueError(
            f"Unknown LLM provider: {settings.llm_provider}. "
            "Set LLM_PROVIDER to 'gemini', 'ollama', or 'openrouter' in .env"
        )
