# FastAPI RAG Chatbot - Simplified Structure

## Directory Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app with all endpoints
│   │
│   ├── core/                    # Core application files (flat structure)
│   │   ├── __init__.py
│   │   ├── config.py            # Settings and configuration
│   │   ├── database.py          # Database session and engine
│   │   ├── models.py            # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   │
│   ├── rag/                     # RAG-related files
│   │   ├── __init__.py
│   │   ├── agent.py             # Chat agent with LangChain
│   │   ├── embeddings.py        # Embeddings and vector store
│   │   └── prompts.py           # Prompt templates
│   │
│   └── services/                # Business logic services
│       ├── __init__.py
│       ├── chat.py              # Chat service
│       └── scraper.py           # Web scraping service
│
├── alembic/                     # Database migrations
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── alembic.ini
```

## File Descriptions

### Core (`app/core/`)
- **config.py**: Application settings using Pydantic BaseSettings
- **database.py**: Async SQLAlchemy engine, session factory, and Base model
- **models.py**: Database models (Document, Conversation, Message)
- **schemas.py**: Pydantic schemas for request/response validation

### Services (`app/services/`)
- **chat.py**: Chat service handling conversations and messages
- **scraper.py**: Web scraping service using Firecrawl

### Main (`app/main.py`)
FastAPI application with endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - Chat with AI
- `POST /chat` - Chat with AI

## Benefits of This Structure

✅ **Simple**: Only 3 main folders, easy to navigate  
✅ **Scalable**: Can add more files to each folder as needed  
✅ **Clear Separation**: Core, RAG, and Services are distinct  
✅ **Flat Structure**: No deep nesting, files are easy to find  
✅ **Modular**: Each file has a single responsibility  

## Usage

```bash
# Run the application
uv run uvicorn app.main:app --reload

# Access API docs
http://localhost:8000/docs
```
