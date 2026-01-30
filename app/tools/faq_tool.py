from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from app.core.database import SessionLocal
from app.core.models import FAQ
from sqlalchemy.future import select

class FAQInput(BaseModel):
    question: str = Field(description="User's question to search in FAQs")

def search_faq_func(question: str) -> str:
    """Search predefined FAQs for E2M Solutions."""
    with SessionLocal() as session:
        query = select(FAQ).where(FAQ.question.ilike(f"%{question}%"))
        result = session.execute(query).scalars().first()
        
        if result:
            return result.answer
        return "NO_MATCH"

search_faq_tool = StructuredTool.from_function(
    func=search_faq_func,
    name="search_faq",
    description="Search predefined FAQs for E2M Solutions. Use this FIRST before other tools.",
    args_schema=FAQInput
)
