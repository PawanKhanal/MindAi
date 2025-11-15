Setup Instructions
Clone and setup:

bash
git clone <your-repo>
cd rag_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Set environment variables:

bash
cp .env.example .env
# Edit .env with your API keys
Run services:

bash
# Start Redis
docker run -d -p 6379:6379 redis:alpine

# Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
API Usage Examples
Document Ingestion
bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@document.pdf" \
  -F "chunking_strategy=fixed_size"
Conversational RAG
bash
curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the document about?",
    "session_id": "user123"
  }'
Direct Interview Booking
bash
curl -X POST "http://localhost:8000/api/v1/chat/book-interview" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-01-15",
    "time": "14:30"
  }'