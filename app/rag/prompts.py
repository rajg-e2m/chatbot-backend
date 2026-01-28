"""Prompt Templates for RAG"""

from langchain.prompts import PromptTemplate


# System prompt for the chat agent
SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided context.
Use the following pieces of context to answer the user's question.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the sources you used to answer the question.

Context: {context}

Question: {question}

Answer:"""


# Prompt template for conversational retrieval
CONVERSATIONAL_PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"]
)


# Prompt for document summarization
SUMMARIZATION_PROMPT = """Please provide a concise summary of the following text:

{text}

Summary:"""


# Prompt for extracting key information
EXTRACTION_PROMPT = """Extract the key information from the following text:

{text}

Key Information:"""
