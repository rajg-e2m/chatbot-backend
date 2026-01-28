from sqlalchemy.future import select
from app.core.database import SessionLocal
from app.core.models import Lead
from uuid import UUID

async def create_lead(name: str, email: str, phone: str) -> Lead:
    """Create a new lead in the database."""
    with SessionLocal() as session:
        lead = Lead(name=name, email=email, phone=phone)
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead

async def get_lead_by_email(email: str) -> Lead | None:
    """Retrieve a lead by email."""
    with SessionLocal() as session:
        query = select(Lead).where(Lead.email == email)
        return session.execute(query).scalars().first()

async def update_lead_intent(lead_id: UUID, intent: str):
    """Update the intent classification for a lead."""
    with SessionLocal() as session:
        query = select(Lead).where(Lead.id == lead_id)
        lead = session.execute(query).scalars().first()
        if lead:
            lead.intent_classification = intent
            session.commit()
            session.refresh(lead)
