from pydantic import BaseModel, Field
from enum import Enum

class ChunkingStrategy(str, Enum):
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"

class DocumentUpload(BaseModel):
    chunking_strategy: ChunkingStrategy = Field(default=ChunkingStrategy.FIXED_SIZE)

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    status: str

class ChatMessage(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: list[str] = []

class InterviewBooking(BaseModel):
    name: str
    email: str
    date: str
    time: str

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    details: InterviewBooking