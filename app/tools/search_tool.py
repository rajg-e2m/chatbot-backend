from langchain_tavily import TavilySearch
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Only initialize if API key is provided
if settings.TAVILY_API_KEY and settings.TAVILY_API_KEY.strip():
    tavily_search_tool = TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        tavily_api_key=settings.TAVILY_API_KEY
    )
else:
    logger.warning("TAVILY_API_KEY not found. Search tool will be disabled or limited.")
    # Create a dummy tool or a mock
    from langchain_core.tools import tool
    
    @tool
    def tavily_search_results(query: str) -> str:
        """Search the web for information. (Disabled: Missing API Key)"""
        return "Search functionality is currently disabled. Please provide a TAVILY_API_KEY in the .env file."
    
    tavily_search_tool = tavily_search_results
