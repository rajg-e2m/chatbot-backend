"""Test script to verify all critical imports"""

try:
    print("Testing imports...")
    
    # Core framework
    import fastapi
    print(f"[OK] FastAPI {fastapi.__version__}")
    
    import uvicorn
    print(f"[OK] Uvicorn installed")
    
    # LangChain ecosystem
    import langchain
    print(f"[OK] LangChain {langchain.__version__}")
    
    import langchain_core
    print(f"[OK] LangChain Core installed")
    
    import langchain_community
    print(f"[OK] LangChain Community installed")
    
    import langchain_huggingface
    print(f"[OK] LangChain HuggingFace installed")
    
    import langgraph
    print(f"[OK] LangGraph installed")
    
    from langgraph.checkpoint.postgres import PostgresSaver
    print(f"[OK] LangGraph PostgreSQL Checkpoint Saver")
    
    # Database
    import sqlalchemy
    print(f"[OK] SQLAlchemy {sqlalchemy.__version__}")
    
    import asyncpg
    print(f"[OK] AsyncPG installed")
    
    import psycopg2
    print(f"[OK] Psycopg2 installed")
    
    # Configuration
    import pydantic
    print(f"[OK] Pydantic {pydantic.__version__}")
    
    from pydantic_settings import BaseSettings
    print(f"[OK] Pydantic Settings")
    
    # Firecrawl
    from firecrawl import FirecrawlApp
    print(f"[OK] Firecrawl SDK")
    
    # Vector store
    import pgvector
    print(f"[OK] PGVector installed")
    
    print("\n[SUCCESS] All imports successful!")
    print("[SUCCESS] FastAPI RAG Chatbot backend is ready!")
    
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    exit(1)
