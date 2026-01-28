from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.schemas import ChatRequest, ChatResponse, ChatInitRequest, LeadRegisterRequest
from app.services import process_message, init_chat, register_lead

app = FastAPI(
    title="E2M Solutions Lead-Generating Chatbot",
    description="A professional sales assistant for E2M Solutions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "E2M Solutions Lead-Generating Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "E2M-Chatbot"}


@app.post("/chat/init", response_model=ChatResponse)
async def initialize_chat(request: ChatInitRequest):
    try:
        result = await init_chat(thread_id=request.thread_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/register")
async def register(request: LeadRegisterRequest):
    try:
        result = await register_lead(
            name=request.name,
            email=request.email,
            phone=request.phone,
            thread_id=request.thread_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await process_message(
            message=request.message,
            thread_id=request.thread_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
