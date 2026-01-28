from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from app.core.config import settings
from app.tools.faq_tool import search_faq_tool
from app.tools.scraper_tool import scrape_website_tool
from app.tools.intent_tool import classify_intent_tool
from app.tools.search_tool import tavily_tool
from langchain_core.messages import HumanMessage
import psycopg

def get_llm():
    """Get the LLM instance based on configuration."""
    # Using HuggingFace as configured in config.py
    llm = HuggingFaceEndpoint(
        repo_id=settings.HF_MODEL,
        huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
        task="text-generation",
    )
    return ChatHuggingFace(llm=llm)

def get_checkpointer():
    """Create a PostgresSaver checkpointer."""
    # langgraph-checkpoint-postgres uses a connection pool or connection string
    # We need to use the sync connection string for psycopg
    return PostgresSaver.from_conn_string(settings.DATABASE_URL)

def create_e2m_agent():
    """Create the LangGraph agent with tools and checkpointing."""
    tools = [
        search_faq_tool,
        scrape_website_tool,
        classify_intent_tool,
        tavily_tool
    ]
    
    system_prompt = """You are a professional sales assistant for E2M Solutions (https://www.e2msolutions.com/).

RULES:
1. ALWAYS check FAQs first using search_faq tool.
2. If FAQ returns NO_MATCH, use scrape_e2m_website tool to find information on the E2M website.
3. NEVER hallucinate pricing or services not found in tools.
4. Classify user intent using classify_user_intent tool based on the user's message.
5. Be professional, helpful, and concise.
6. Answer ONLY about E2M Solutions and its services.

If you cannot find information, politely suggest contacting E2M directly through their website."""
    
    llm = get_llm()
    checkpointer = get_checkpointer()
    
    # create_react_agent is the modern way to create an agent in LangGraph
    return create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt,
        checkpointer=checkpointer
    )

async def chat(message: str, thread_id: str):
    """Process a chat message through the agent."""
    agent = create_e2m_agent()
    config = {"configurable": {"thread_id": thread_id}}
    
    # Setup the database for LangGraph checkpointer if it hasn't been done
    # PostgresSaver.setup(settings.DATABASE_URL) # This usually needs to run once
    
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    return {
        "answer": result["messages"][-1].content,
        "thread_id": thread_id
    }
