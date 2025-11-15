from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.api import documents, chat
from app.models.database import create_tables

load_dotenv()

app = FastAPI(
    title="RAG Backend API",
    description="Document Ingestion and Conversational RAG System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1/documents", tags=["Document Ingestion"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Conversational RAG"])

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "RAG Backend API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}