"""Pydantic Schemas for Request/Response Validation"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional, List


# Document Schemas
class DocumentBase(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    content: str


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Chat Schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    conversation_id: UUID
    message: str
    sources: Optional[List[str]] = None


# Scrape Schemas
class ScrapeRequest(BaseModel):
    url: HttpUrl


class ScrapeResponse(BaseModel):
    url: str
    title: Optional[str] = None
    content: str
    status: str
