"""Chat Service"""

from app.rag.agent import chat_agent
from app.core.models import Conversation, Message
from app.core.database import AsyncSessionLocal
from uuid import UUID, uuid4


class ChatService:
    """Service for handling chat operations"""
    
    async def process_message(self, user_message: str, conversation_id: UUID = None) -> dict:
        """Process a chat message"""
        # Create or get conversation
        async with AsyncSessionLocal() as session:
            if conversation_id:
                conversation = await session.get(Conversation, conversation_id)
            else:
                conversation = Conversation(id=uuid4())
                session.add(conversation)
                await session.commit()
                await session.refresh(conversation)
            
            # Save user message
            user_msg = Message(
                conversation_id=conversation.id,
                role="user",
                content=user_message
            )
            session.add(user_msg)
            await session.commit()
        
        # Get response from chat agent
        response = await chat_agent.chat(user_message, str(conversation_id))
        
        # Save assistant message
        async with AsyncSessionLocal() as session:
            assistant_msg = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response["answer"]
            )
            session.add(assistant_msg)
            await session.commit()
        
        return {
            "conversation_id": conversation.id,
            "message": response["answer"],
            "sources": response.get("sources", [])
        }


# Global chat service instance
chat_service = ChatService()
