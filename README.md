# FastAPI E2M Chatbot Backend

A professional FastAPI backend for a tool-powered chatbot with on-the-go web scraping and FAQ search capabilities.

## Features
- 🚀 FastAPI 0.128.0 with async support
- ⚡ Astral UV for fast package management
- 🤖 LangChain/LangGraph for Agent implementation
- 🔍 On-the-go FAQ search via SQL
- 🌐 Real-time web scraping via Firecrawl
- 🎯 Intent classification for lead prioritization
- 🗄️ PostgreSQL database for lead and conversation tracking
- 🔄 Conversation checkpointing with LangGraph

## Setup
1. Install UV: `pip install uv`
2. Navigate to project: `cd chatbot-e2m/backend`
3. Install dependencies: `uv sync`
4. Copy `.env.example` to `.env` and configure keys
5. Run: `uv run uvicorn app.main:app --reload`

## Architecture
The chatbot uses a Tool-Calling Agent architecture:
1. **FAQ Search**: First, it checks the local database for matching questions.
2. **Web Scraping**: If no match is found, it uses Firecrawl to fetch relevant content from the E2M website.
3. **Intent Classification**: Every interaction is analyzed to classify user intent (HIGH, MEDIUM, LOW).

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
