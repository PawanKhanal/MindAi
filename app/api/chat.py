from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse, InterviewBooking, BookingResponse
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/query", response_model=ChatResponse)
async def chat_query(message: ChatMessage):
    """Handle conversational RAG queries"""
    try:
        if not message.session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        
        result = rag_service.process_query(message.message, message.session_id)
        
        return ChatResponse(
            response=result["response"],
            session_id=message.session_id,
            sources=result["sources"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/book-interview", response_model=BookingResponse)
async def book_interview(booking: InterviewBooking):
    """Direct interview booking endpoint"""
    try:
        booking_id = rag_service.store_booking(booking.dict(), "direct_booking")
        
        return BookingResponse(
            booking_id=booking_id,
            status="confirmed",
            details=booking
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error booking interview: {str(e)}")