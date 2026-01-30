# FastAPI Tool-Based Chatbot - Structure

## Directory Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app with all endpoints
│   │
│   ├── agents/                  # LangChain/LangGraph agents
│   │   ├── chat_agent.py        # Core agent logic
│   │   └── prompts.py           # Agent system prompts
│   │
│   ├── core/                    # Core application files
│   │   ├── __init__.py
│   │   ├── config.py            # Settings and configuration
│   │   ├── database.py          # Database session and engine
│   │   ├── exceptions.py        # Custom exceptions
│   │   ├── llm.py               # LLM initialization
│   │   ├── models.py            # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   │
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat processing logic
│   │   └── lead.py              # Lead management logic
│   │
│   └── tools/                   # Agent tools
│       ├── __init__.py
│       ├── faq_tool.py          # SQL-based FAQ search
│       ├── intent_tool.py       # LLM-based intent classification
│       ├── scraper_tool.py      # Firecrawl web scraping
│       └── search_tool.py       # Tavily search (backup)
│
├── alembic/                     # Database migrations
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── alembic.ini
```

## File Descriptions

### Agents (`app/agents/`)
- **chat_agent.py**: Manages the LangGraph agent, state, and tools.
- **prompts.py**: Centralized storage for agent instructions.

### Tools (`app/tools/`)
- **faq_tool.py**: Searches local database for predefined answers.
- **scraper_tool.py**: Scrapes E2M website on-the-go using Firecrawl.
- **intent_tool.py**: Classifies user buying intent (HIGH, MEDIUM, LOW).

### Core (`app/core/`)
- **config.py**: Application settings using Pydantic BaseSettings.
- **database.py**: Async and Sync SQLAlchemy setups.
- **models.py**: Database models (Lead, FAQ, Conversation, etc.).
- **schemas.py**: Pydantic models for validation.

### Main (`app/main.py`)
FastAPI application with endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat/init` - Initialize chat session
- `POST /chat/register` - Register lead information
- `POST /chat` - Chat with the assistant

## Benefits of This Structure

✅ **Modular**: Clear separation between agents, tools, and core logic.
✅ **Scalable**: Easy to add new tools or agent types.
✅ **Robust**: On-the-go information retrieval avoids stale vector indexes.
