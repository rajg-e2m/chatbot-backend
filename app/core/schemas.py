from pydantic import BaseModel, EmailStr
from typing import Optional


class ChatInitRequest(BaseModel):
    thread_id: str


class LeadRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    thread_id: str


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    answer: str
    thread_id: str
    requires_lead_info: bool = False
