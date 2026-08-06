
from config import (
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_LLM_MODEL,
    TEMPERATURE,
)


def get_llm():
    """
    Returns the configured chat model.
    """

    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=OLLAMA_LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=TEMPERATURE,
        )

    elif LLM_PROVIDER == "azure":
        from langchain_openai import AzureChatOpenAI
        from config import (
            AZURE_ENDPOINT,
            AZURE_API_KEY,
            AZURE_API_VERSION,
            AZURE_CHAT_DEPLOYMENT,
        )

        return AzureChatOpenAI(
            azure_endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_deployment=AZURE_CHAT_DEPLOYMENT,
            temperature=TEMPERATURE,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")