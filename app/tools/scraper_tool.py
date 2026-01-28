from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.models import WebsiteContent
from sqlalchemy.future import select
from datetime import datetime

class ScraperInput(BaseModel):
    url: str = Field(description="E2M website URL to scrape")

def scrape_website_func(url: str) -> str:
    """Scrape E2M Solutions website content using Firecrawl."""
    # Check cache first
    with SessionLocal() as session:
        query = select(WebsiteContent).where(WebsiteContent.url == url)
        cached = session.execute(query).scalars().first()
        if cached:
            return cached.content

    # Scrape if not cached
    app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)
    scrape_result = app.scrape_url(url, params={'formats': ['markdown'], 'onlyMainContent': True})
    
    if scrape_result and 'markdown' in scrape_result:
        content = scrape_result['markdown']
        
        # Cache the result
        with SessionLocal() as session:
            new_content = WebsiteContent(url=url, content=content)
            session.add(new_content)
            session.commit()
            
        return content
    
    return "Failed to scrape content."

scrape_website_tool = StructuredTool.from_function(
    func=scrape_website_func,
    name="scrape_e2m_website",
    description="Scrape E2M Solutions website content. Use when FAQ doesn't have answer.",
    args_schema=ScraperInput
)
