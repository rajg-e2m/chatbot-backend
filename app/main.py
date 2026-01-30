from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.schemas import ChatRequest, ChatResponse, ChatInitRequest, LeadRegisterRequest
from app.core.database import get_db
from app.core.exceptions import ChatbotException
from app.services import process_message, init_chat, register_lead
from fastapi.responses import JSONResponse

app = FastAPI(
    title=settings.APP_NAME,
    description="A professional sales assistant for E2M Solutions",
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(ChatbotException)
async def chatbot_exception_handler(request, exc: ChatbotException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )

@app.get("/")
async def root():
    return {
        "message": "E2M Solutions Lead-Generating Chatbot API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "E2M-Chatbot"}

@app.post("/chat/init", response_model=ChatResponse)
async def initialize_chat(
    request: ChatInitRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await init_chat(db=db, thread_id=request.thread_id)
    return result

@app.post("/chat/register")
async def register(
    request: LeadRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await register_lead(
        db=db,
        name=request.name,
        email=request.email,
        phone=request.phone,
        thread_id=request.thread_id
    )
    return result

@app.get("/admin/leads")
async def get_leads(
    db: AsyncSession = Depends(get_db)
):
    from app.services import get_all_leads
    leads = await get_all_leads(db)
    return leads

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await process_message(
        db=db,
        message=request.message,
        thread_id=request.thread_id
    )
    return result
