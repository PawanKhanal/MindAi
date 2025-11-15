PalmMind RAG Backend System
A production-ready Retrieval-Augmented Generation (RAG) backend built with FastAPI, featuring document processing, conversational AI, and interview booking capabilities.

🚀 Features
Document Ingestion: Upload and process PDF/TXT files with multiple chunking strategies

Conversational RAG: Intelligent document search with multi-turn conversation support

Vector Search: Semantic similarity search using Qdrant vector database

Chat Memory: Redis-powered conversation history

Interview Booking: LLM-powered scheduling extraction and storage

RESTful API: Clean, well-documented endpoints

Dockerized: Complete containerization for easy deployment

🛠️ Tech Stack
Backend: FastAPI, Python 3.11

Vector Database: Qdrant

Cache: Redis

Database: SQLite (with SQLAlchemy ORM)

Embeddings: Custom word-frequency based embeddings (no external APIs)

Containerization: Docker & Docker Compose

📋 Prerequisites
Python 3.11+

Docker & Docker Compose

Git

⚡ Quick Start
Method 1: Docker Compose (Recommended)
bash
# Clone the repository
git clone <your-repo>
cd palmmind

# Start all services
docker compose up --build

# Access the application
# API Documentation: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
Method 2: Manual Setup
bash
# Clone and setup
git clone <your-repo>
cd palmmind
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Start Redis
docker run -d -p 6379:6379 redis:alpine

# Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
🔧 Configuration
Environment Variables
Create a .env file with the following variables:

env
DATABASE_URL=sqlite:///./rag_system.db
REDIS_HOST=localhost
REDIS_PORT=6379
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
Docker Services
The system uses three main services:

Redis: Chat memory and session storage (port 6379)

Qdrant: Vector database for embeddings (ports 6333-6334)

FastAPI: Main application server (port 8000)

📚 API Documentation
Once running, access the interactive API documentation at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔌 API Endpoints
Document Ingestion
Upload Document

bash
POST /api/v1/documents/upload

curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@document.pdf" \
  -F "chunking_strategy=fixed_size"
Parameters:

file: PDF or TXT file to upload

chunking_strategy: fixed_size or semantic

Response:

json
{
  "document_id": "uuid-string",
  "filename": "document.pdf",
  "chunk_count": 5,
  "status": "processed"
}
Conversational RAG
Chat Query

bash
POST /api/v1/chat/query

curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is this document about?",
    "session_id": "user123"
  }'
Parameters:

message: User query message

session_id: Unique session identifier for conversation history

Response:

json
{
  "response": "I found relevant information in your documents...",
  "session_id": "user123",
  "sources": [
    "Document (relevance: 0.854)",
    "Document (relevance: 0.732)"
  ],
  "booking_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-01-15",
    "time": "14:30"
  },
  "booking_id": "uuid-string"
}
Interview Booking
Direct Booking

bash
POST /api/v1/chat/book-interview

curl -X POST "http://localhost:8000/api/v1/chat/book-interview" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-01-15",
    "time": "14:30"
  }'
Response:

json
{
  "booking_id": "uuid-string",
  "status": "confirmed",
  "details": {
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-01-15",
    "time": "14:30"
  }
}
🏗️ Project Structure
text
palmmind/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── database.py         # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── services/
│   │   ├── document_ingestion.py
│   │   ├── embedding_service.py
│   │   ├── rag_service.py
│   │   └── chat_memory.py
│   ├── api/
│   │   ├── documents.py        # Document ingestion endpoints
│   │   └── chat.py             # Chat and booking endpoints
│   └── utils/
│       ├── chunking.py         # Text chunking strategies
│       └── file_processing.py  # File type handling
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
🔍 Core Components
Document Processing Pipeline
File Upload: Accepts PDF and TXT files

Text Extraction: Converts files to plain text

Chunking: Splits text using fixed-size or semantic strategies

Embedding Generation: Creates vector embeddings using custom algorithms

Vector Storage: Stores embeddings in Qdrant for similarity search

Conversational RAG
Semantic Search: Finds relevant document chunks based on query similarity

Context Management: Maintains conversation history using Redis

Response Generation: Provides contextual answers based on document content

Multi-turn Support: Handles follow-up questions with conversation context

Interview Booking
Pattern Recognition: Extracts booking details from natural language

Data Validation: Ensures required fields are present

Database Storage: Persists booking information

Confirmation: Returns booking IDs for reference

🐳 Docker Commands
bash
# Start all services
docker compose up --build

# Start in detached mode
docker compose up -d

# View logs
docker compose logs -f palmmind-app

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Check service status
docker compose ps
🧪 Testing
Health Check
bash
curl http://localhost:8000/health
Complete System Test
bash
# Create test document
echo "Test document content" > test.txt

# Upload document
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@test.txt" \
  -F "chunking_strategy=fixed_size"

# Test conversation
curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is in the document?", "session_id": "test"}'

# Test booking
curl -X POST "http://localhost:8000/api/v1/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "Schedule interview with test@example.com", "session_id": "test"}'
🔒 Security Features
Input validation using Pydantic schemas

File type restrictions (PDF/TXT only)

SQL injection prevention through ORM

CORS configuration for web clients

Rate limiting ready architecture

📈 Performance
Vector Search: Sub-second response times for document retrieval

Chat Memory: Redis-backed for fast conversation context

Embedding Generation: Custom algorithm for zero external dependencies

Scalability: Containerized architecture for horizontal scaling

🚨 Troubleshooting
Common Issues
Document Upload Fails

Ensure uploads directory exists: mkdir -p uploads

Check file permissions

Verify file is PDF or TXT format

Services Not Connecting

Check Docker is running: docker ps

Verify ports are available: netstat -an | findstr "6333\|6379\|8000"

Restart services: docker compose restart

Memory Issues

Monitor Redis memory: docker compose exec redis redis-cli info memory

Clear chat history if needed

Logs and Debugging
bash
# View application logs
docker compose logs palmmind-app

# Check Redis connectivity
docker compose exec redis redis-cli ping

# Test Qdrant health
curl http://localhost:6333
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
FastAPI for the excellent web framework

Qdrant for the vector search capabilities

Redis for in-memory data storage

SQLAlchemy for database ORM