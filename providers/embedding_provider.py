
from config import (
    EMBEDDING_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL,
)


def get_embeddings():
    """
    Returns the configured embedding model.
    """

    if EMBEDDING_PROVIDER == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

    elif EMBEDDING_PROVIDER == "azure":
        from langchain_openai import AzureOpenAIEmbeddings
        from config import (
            AZURE_ENDPOINT,
            AZURE_API_KEY,
            AZURE_API_VERSION,
            AZURE_EMBEDDING_DEPLOYMENT,
        )

        return AzureOpenAIEmbeddings(
            azure_endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
        )

    else:
        raise ValueError(
            f"Unsupported embedding provider: {EMBEDDING_PROVIDER}"
        )