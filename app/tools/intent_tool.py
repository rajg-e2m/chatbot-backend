from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class IntentInput(BaseModel):
    message: str = Field(description="User message to classify intent")

def classify_intent_func(message: str) -> str:
    """Classify user's buying intent as HIGH, MEDIUM, or LOW"""
    msg = message.lower()
    
    high_intent_keywords = ['pricing', 'cost', 'quote', 'hire', 'service', 'budget', 'proposal']
    medium_intent_keywords = ['capabilities', 'experience', 'portfolio', 'how do you', 'can you']
    
    if any(keyword in msg for keyword in high_intent_keywords):
        return "HIGH"
    elif any(keyword in msg for keyword in medium_intent_keywords):
        return "MEDIUM"
    else:
        return "LOW"

classify_intent_tool = StructuredTool.from_function(
    func=classify_intent_func,
    name="classify_user_intent",
    description="Classify user's buying intent as HIGH, MEDIUM, or LOW",
    args_schema=IntentInput
)
