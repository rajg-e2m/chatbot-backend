# FastAPI RAG Chatbot Backend

A production-ready FastAPI backend for a RAG-powered chatbot with web scraping capabilities.

## Features
- 🚀 FastAPI 0.128.0 with async support
- ⚡ Astral UV for fast package management
- 🤖 LangChain/LangGraph for RAG implementation
- 🗄️ Supabase PostgreSQL database
- 🔄 Conversation checkpointing
- 🌐 Firecrawl for web scraping
- 🤗 HuggingFace for embeddings and LLMs
- 📊 Vector similarity search with pgvector

## Setup
1. Install UV: `pip install uv`
2. Navigate to project: `cd c:\Users\Developer\Desktop\Hello\chatbot-e2m\backend`
3. Install dependencies: `uv sync`
4. Copy `.env.example` to `.env` and configure
5. Run: `uv run uvicorn app.main:app --reload`

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
