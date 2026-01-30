from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from app.core.config import settings

def get_llm():
    """Get the LLM instance based on configuration."""
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=settings.HF_MODEL,
        huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
        task="text-generation",
    )
    return ChatHuggingFace(llm=llm_endpoint)
