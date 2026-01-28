from langchain_community.tools.tavily_search import TavilySearchResults
from app.core.config import settings

tavily_tool = TavilySearchResults(
    max_results=3,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    api_key=settings.TAVILY_API_KEY
)
