import uuid
from typing import Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Conversation, Message
from app.agents.chat_agent import chat
from app.core.exceptions import LeadRegistrationRequiredException
from app.services.lead import create_lead

async def init_chat(db: AsyncSession, thread_id: str) -> Dict[str, Any]:
    """Initialize a chat session. Checks if lead info is required."""
    conv_id = uuid.UUID(thread_id)
    query = select(Conversation).where(Conversation.id == conv_id)
    result = await db.execute(query)
    conversation = result.scalars().first()

    if not conversation or not conversation.lead_id:
        return {
            "requires_lead_info": True,
            "answer": "Can you please provide your phone number, email, and name first so that I can provide you further information?",
            "thread_id": thread_id
        }

    return {
        "requires_lead_info": False,
        "answer": "Welcome back! How can I help you today?",
        "thread_id": thread_id
    }

async def register_lead(db: AsyncSession, name: str, email: str, phone: str, thread_id: str) -> Dict[str, Any]:
    """Register a new lead and associate it with a conversation."""
    lead = await create_lead(db, name, email, phone)
    
    conv_id = uuid.UUID(thread_id)
    query = select(Conversation).where(Conversation.id == conv_id)
    result = await db.execute(query)
    conversation = result.scalars().first()

    if conversation:
        conversation.lead_id = lead.id
    else:
        conversation = Conversation(id=conv_id, lead_id=lead.id)
        db.add(conversation)
        
    await db.commit()
    return {"registered": True, "thread_id": thread_id}

async def process_message(db: AsyncSession, message: str, thread_id: str) -> Dict[str, Any]:
    """Process a user message through the agent and store the conversation."""
    conv_id = uuid.UUID(thread_id)
    query = select(Conversation).where(Conversation.id == conv_id)
    result = await db.execute(query)
    conversation = result.scalars().first()

    if not conversation or not conversation.lead_id:
        raise LeadRegistrationRequiredException()

    # 1. Store human message
    human_msg = Message(conversation_id=conv_id, role="user", content=message)
    db.add(human_msg)
    await db.commit()
    
    # 2. Get agent response
    response = await chat(message, thread_id)
    
    # 3. Store assistant response
    ai_msg = Message(conversation_id=conv_id, role="assistant", content=response["answer"])
    db.add(ai_msg)
    await db.commit()
        
    return response
