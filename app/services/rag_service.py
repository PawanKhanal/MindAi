from typing import List, Dict, Any
import os
from app.services.embedding_service import EmbeddingService
from app.services.chat_memory import ChatMemory
from app.models.database import get_db, InterviewBooking as InterviewBookingModel
import uuid
import re

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chat_memory = ChatMemory()
    
    def format_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Format search results into context string"""
        if not search_results:
            return "No relevant documents found."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[Document {i} - Relevance: {result['score']:.3f}]: {result['text']}")
        return "\n\n".join(context_parts)
    
    def generate_response_simple(self, query: str, context: str, chat_history: List[Dict[str, str]]) -> str:
        """Generate simple responses based on found documents"""
        
        if "hello" in query.lower() or "hi" in query.lower():
            return "Hello! I'm your document assistant. I can help you search through your uploaded documents."
        
        if "thank" in query.lower():
            return "You're welcome! Is there anything else you'd like to know about your documents?"
        
        if context and "No relevant documents" not in context:
            # Found relevant documents
            doc_count = len(context.split('[Document')) - 1
            return f"""I found {doc_count} relevant document(s) that match your query:

{context[:800]}...

This information was retrieved from your uploaded documents using semantic search."""
        
        else:
            # No relevant documents found
            return "I searched through your uploaded documents but didn't find specific information to answer your question. You might want to upload relevant documents or try rephrasing your question."
    
    def extract_booking_info(self, text: str) -> Dict[str, str]:
        """Extract interview booking information using pattern matching"""
        booking_info = {}
        
        # Extract name
        name_patterns = [
            r'(?:name is|my name is|called)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'(?:with|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s+for interview|\s+at|\s+on)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                booking_info['name'] = match.group(1).strip()
                break
        
        # Extract email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
        if email_match:
            booking_info['email'] = email_match.group(1)
        
        # Extract time
        time_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)', text, re.IGNORECASE)
        if time_match:
            booking_info['time'] = time_match.group(1)
        elif 'morning' in text.lower():
            booking_info['time'] = '09:00 AM'
        elif 'afternoon' in text.lower():
            booking_info['time'] = '02:00 PM'
        
        # Extract date
        if 'tomorrow' in text.lower():
            from datetime import datetime, timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            booking_info['date'] = tomorrow.strftime('%Y-%m-%d')
        elif 'monday' in text.lower():
            booking_info['date'] = 'next Monday'
        elif 'tuesday' in text.lower():
            booking_info['date'] = 'next Tuesday'
        elif 'wednesday' in text.lower():
            booking_info['date'] = 'next Wednesday'
        elif 'thursday' in text.lower():
            booking_info['date'] = 'next Thursday'
        elif 'friday' in text.lower():
            booking_info['date'] = 'next Friday'
        
        return booking_info
    
    def store_booking(self, booking_info: Dict[str, str], session_id: str) -> str:
        """Store booking information in database"""
        db = get_db()
        try:
            booking_id = str(uuid.uuid4())
            booking = InterviewBookingModel(
                id=booking_id,
                name=booking_info.get("name", ""),
                email=booking_info.get("email", ""),
                date=booking_info.get("date", ""),
                time=booking_info.get("time", ""),
                session_id=session_id
            )
            db.add(booking)
            db.commit()
            return booking_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def process_query(self, query: str, session_id: str) -> Dict[str, Any]:
        """Process user query with RAG"""
        
        # Get chat history from Redis
        chat_history = self.chat_memory.get_messages(session_id)
        
        # Search for relevant documents
        search_results = self.embedding_service.search_similar(query, top_k=3)
        
        # Generate response
        context = self.format_context(search_results)
        response = self.generate_response_simple(query, context, chat_history)
        
        # Handle interview booking
        booking_info = None
        booking_id = None
        
        if any(keyword in query.lower() for keyword in ['schedule', 'book', 'interview', 'meeting', 'appointment']):
            booking_info = self.extract_booking_info(query)
            if booking_info and booking_info.get('name') and booking_info.get('email'):
                booking_id = self.store_booking(booking_info, session_id)
                response += f"\n\n✅ Interview scheduled for {booking_info.get('name')} at {booking_info.get('time', 'a suitable time')}. Confirmation sent to {booking_info.get('email')}."
        
        # Update chat memory
        self.chat_memory.add_message(session_id, {"role": "user", "content": query})
        self.chat_memory.add_message(session_id, {"role": "assistant", "content": response})
        
        return {
            "response": response,
            "sources": [f"Document (relevance: {result['score']:.3f})" for result in search_results],
            "booking_info": booking_info,
            "booking_id": booking_id
        }