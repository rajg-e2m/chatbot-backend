"""FastAPI RAG Chatbot - Main Application Entry Point"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.schemas import ChatRequest, ChatResponse, ScrapeRequest, ScrapeResponse
from app.services import chat_service, scraper_service

app = FastAPI(
    title="FastAPI RAG Chatbot",
    description="A RAG-powered chatbot with web scraping capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastAPI RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "FastAPI RAG Chatbot"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint - send a message and get AI response"""
    try:
        result = await chat_service.process_message(
            user_message=request.message,
            conversation_id=request.conversation_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    """Scrape a URL and add to knowledge base"""
    try:
        result = await scraper_service.scrape_url(str(request.url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
