from sqlalchemy.future import select
from app.core.database import SessionLocal
from app.core.models import Conversation, Message, Lead
from app.agents.chat_agent import chat
from app.services.lead import create_lead
from uuid import UUID
import uuid

async def init_chat(thread_id: str) -> dict:
    """Initialize a chat session. Checks if lead info is required."""
    with SessionLocal() as session:
        query = select(Conversation).where(Conversation.id == uuid.UUID(thread_id))
        conversation = session.execute(query).scalars().first()
        
        if not conversation or not conversation.lead_id:
            return {
                "requires_lead_info": True,
                "message": "Can you please provide your phone number, email, and name first so that I can provide you further information?",
                "thread_id": thread_id
            }
        
    return {
        "requires_lead_info": False,
        "message": "Welcome back! How can I help you today?",
        "thread_id": thread_id
    }

async def register_lead(name: str, email: str, phone: str, thread_id: str) -> dict:
    """Register a new lead and associate it with a conversation."""
    lead = await create_lead(name=name, email=email, phone=phone)
    
    with SessionLocal() as session:
        # Check if conversation exists, update it, or create a new one
        conv_id = uuid.UUID(thread_id)
        query = select(Conversation).where(Conversation.id == conv_id)
        conversation = session.execute(query).scalars().first()
        
        if conversation:
            conversation.lead_id = lead.id
        else:
            conversation = Conversation(id=conv_id, lead_id=lead.id)
            session.add(conversation)
            
        session.commit()
        
    return {"registered": True, "thread_id": thread_id}

async def process_message(message: str, thread_id: str) -> dict:
    """Process a user message through the agent and store the conversation."""
    # 1. Check if lead is registered
    with SessionLocal() as session:
        conv_id = uuid.UUID(thread_id)
        query = select(Conversation).where(Conversation.id == conv_id)
        conversation = session.execute(query).scalars().first()
        
        if not conversation or not conversation.lead_id:
            return {
                "error": "Lead registration required",
                "requires_lead_info": True
            }
        
        # 2. Store human message
        human_msg = Message(conversation_id=conv_id, role="user", content=message)
        session.add(human_msg)
        session.commit()
    
    # 3. Get agent response
    response = await chat(message, thread_id)
    
    # 4. Store assistant response
    with SessionLocal() as session:
        ai_msg = Message(conversation_id=conv_id, role="assistant", content=response["answer"])
        session.add(ai_msg)
        session.commit()
        
    return response
