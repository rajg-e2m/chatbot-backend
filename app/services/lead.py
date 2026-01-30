from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Lead
from uuid import UUID
from typing import Optional

async def create_lead(db: AsyncSession, name: str, email: str, phone: str) -> Lead:
    """Create a new lead in the database."""
    query = select(Lead).where(Lead.email == email)
    result = await db.execute(query)
    existing_lead = result.scalars().first()

    if existing_lead:
        return existing_lead

    lead = Lead(name=name, email=email, phone=phone)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead

async def get_lead_by_email(db: AsyncSession, email: str) -> Optional[Lead]:
    """Retrieve a lead by email."""
    query = select(Lead).where(Lead.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def update_lead_intent(db: AsyncSession, lead_id: UUID, intent: str):
    """Update the intent classification for a lead."""
    query = select(Lead).where(Lead.id == lead_id)
    result = await db.execute(query)
    lead = result.scalars().first()
    if lead:
        lead.intent_classification = intent
        await db.commit()
        await db.refresh(lead)
