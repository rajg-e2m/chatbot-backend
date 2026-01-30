from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from app.agents.prompts import INTENT_CLASSIFICATION_PROMPT
from app.core.llm import get_llm

class IntentInput(BaseModel):
    message: str = Field(description="User message to classify intent")

def classify_intent_func(message: str) -> str:
    """Classify user's buying intent as HIGH, MEDIUM, or LOW using LLM."""
    try:
        llm = get_llm()
        prompt = INTENT_CLASSIFICATION_PROMPT.format(message=message)
        response = llm.invoke(prompt)
        content = response.content.upper().strip()

        # Look for the keywords specifically to avoid issues with conversational filler
        if any(word in content for word in ["HIGH", "INTENT: HIGH"]):
            return "HIGH"
        elif any(word in content for word in ["MEDIUM", "INTENT: MEDIUM"]):
            return "MEDIUM"
        elif any(word in content for word in ["LOW", "INTENT: LOW"]):
            return "LOW"

        # Fallback to simple containment if exact match not found
        if "HIGH" in content: return "HIGH"
        if "MEDIUM" in content: return "MEDIUM"
        return "LOW"
    except Exception:
        # Fallback to keyword search if LLM fails
        msg = message.lower()
        high_intent_keywords = ['pricing', 'cost', 'quote', 'hire', 'service', 'budget', 'proposal', 'estimate']
        medium_intent_keywords = ['capabilities', 'experience', 'portfolio', 'how do you', 'can you', 'about']

        if any(keyword in msg for keyword in high_intent_keywords):
            return "HIGH"
        elif any(keyword in msg for keyword in medium_intent_keywords):
            return "MEDIUM"
        else:
            return "LOW"

classify_intent_tool = StructuredTool.from_function(
    func=classify_intent_func,
    name="classify_user_intent",
    description="Classify user's buying intent as HIGH, MEDIUM, or LOW to help tailor the response.",
    args_schema=IntentInput
)
