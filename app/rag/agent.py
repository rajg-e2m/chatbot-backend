"""RAG Chat Agent"""

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_postgres import PGVector
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from app.core.database import engine


class ChatAgent:
    """RAG-powered chat agent using LangChain"""
    
    def __init__(self):
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.chain = None
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings, LLM, and vector store"""
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize LLM
        self.llm = HuggingFaceEndpoint(
            repo_id=settings.HF_MODEL,
            huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # Initialize vector store
        self.vectorstore = PGVector(
            embeddings=self.embeddings,
            connection=settings.SYNC_DATABASE_URL,
            collection_name="documents"
        )
        
        # Initialize conversation memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create conversational retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True
        )
    
    async def chat(self, message: str, conversation_id: str = None):
        """Process chat message and return response"""
        result = await self.chain.ainvoke({"question": message})
        
        return {
            "answer": result["answer"],
            "sources": [doc.metadata.get("source") for doc in result.get("source_documents", [])]
        }


# Global chat agent instance
chat_agent = ChatAgent()
