"""Embeddings Management"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import settings
from typing import List


class EmbeddingsManager:
    """Manage document embeddings and vector store"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        self.vectorstore = PGVector(
            embeddings=self.embeddings,
            connection=settings.SYNC_DATABASE_URL,
            collection_name="documents"
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    async def add_document(self, content: str, metadata: dict):
        """Add document to vector store"""
        # Split text into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Add to vector store
        await self.vectorstore.aadd_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks)
        )
    
    async def search(self, query: str, k: int = 3) -> List[dict]:
        """Search for similar documents"""
        results = await self.vectorstore.asimilarity_search(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ]


# Global embeddings manager instance
embeddings_manager = EmbeddingsManager()
