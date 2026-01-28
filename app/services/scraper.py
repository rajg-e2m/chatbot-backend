"""Web Scraping Service using Firecrawl"""

from firecrawl import FirecrawlApp
from app.core.config import settings
from app.core.models import Document
from app.core.database import AsyncSessionLocal
from app.rag.embeddings import embeddings_manager
from sqlalchemy import select


class ScraperService:
    """Service for web scraping using Firecrawl"""
    
    def __init__(self):
        self.firecrawl = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)
    
    async def scrape_url(self, url: str) -> dict:
        """Scrape a URL and store in database"""
        # Scrape using Firecrawl
        result = self.firecrawl.scrape(url, formats=["markdown"])
        
        # Extract content
        content = result.get("markdown", "")
        title = result.get("metadata", {}).get("title", "")
        
        # Store in database
        async with AsyncSessionLocal() as session:
            # Check if document already exists
            stmt = select(Document).where(Document.url == url)
            existing_doc = await session.execute(stmt)
            existing_doc = existing_doc.scalar_one_or_none()
            
            if existing_doc:
                # Update existing document
                existing_doc.content = content
                existing_doc.title = title
                doc = existing_doc
            else:
                # Create new document
                doc = Document(url=url, title=title, content=content)
                session.add(doc)
            
            await session.commit()
            await session.refresh(doc)
        
        # Add to vector store
        await embeddings_manager.add_document(
            content=content,
            metadata={"source": url, "title": title}
        )
        
        return {
            "url": url,
            "title": title,
            "content": content,
            "status": "success"
        }


# Global scraper service instance
scraper_service = ScraperService()
