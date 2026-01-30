from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents import create_agent
from app.core.config import settings
from app.tools.faq_tool import search_faq_tool
from app.tools.scraper_tool import scrape_website_tool
from app.tools.intent_tool import classify_intent_tool

from langchain_core.messages import HumanMessage
from app.agents.prompts import SYSTEM_PROMPT
from typing import Dict, Any

# Global agent instance for caching
_agent = None

from app.core.llm import get_llm

def get_checkpointer():
    """Create a PostgresSaver checkpointer."""
    return PostgresSaver.from_conn_string(settings.DATABASE_URL)

def create_e2m_agent():
    """Create the LangGraph agent with tools and checkpointing."""
    tools = [
        search_faq_tool,
        scrape_website_tool,
        classify_intent_tool
    ]
    
    llm = get_llm()
    checkpointer = get_checkpointer()
    
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

def get_agent():
    """Get or create the cached agent instance."""
    global _agent
    if _agent is None:
        _agent = create_e2m_agent()
    return _agent

async def chat(message: str, thread_id: str) -> Dict[str, Any]:
    """Process a chat message through the agent."""
    agent = get_agent()
    config = {"configurable": {"thread_id": thread_id}}
    
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    return {
        "answer": result["messages"][-1].content,
        "thread_id": thread_id
    }
