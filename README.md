# PalmMind RAG Backend System

PalmMind is a production-ready Retrieval-Augmented Generation (RAG) backend built with FastAPI.  
It supports document ingestion, semantic search, conversational chat, and automated interview booking — all using fully local infrastructure (Qdrant, Redis, Docker).


## 🚀 Features

- **Document Ingestion** – Upload and process PDF/TXT files with flexible chunking strategies  
- **Conversational RAG** – Multi-turn intelligent querying over document knowledge  
- **Vector Search** – Qdrant-backed semantic search  
- **Chat Memory** – Redis-powered conversation history  
- **Interview Booking** – LLM-assisted extraction & storage of scheduling details  
- **REST API** – Clean, modular FastAPI endpoints  
- **Dockerized Deployment** – Fully containerized services


## 🛠️ Tech Stack

- **Backend:** FastAPI (Python 3.11)
- **Vector DB:** Qdrant
- **Cache / Memory:** Redis
- **Database:** SQLite + SQLAlchemy ORM
- **Embeddings:** Local word-frequency embedding (no external APIs)
- **Deployment:** Docker & Docker Compose

---
## ⚙️ Quick Setup
```bash
# 1. Clone the repository
git clone <repo-url>
cd palmmind

# 2. Copy env template and configure
cp .env.example .env
# (Edit .env as needed)

# 3. Start Docker dependencies (Redis + Qdrant)
docker compose up -d

# 4. Create Python virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 5. Install all dependencies
pip install -r requirements.txt

# 6. Initialize the local database (auto-created for SQLite)
# No migrations needed — SQLAlchemy handles table creation
# But ensure the file exists:
touch rag_system.db  # Linux/Mac
type nul > rag_system.db  # Windows PowerShell

# 7. Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


## ⚡ Manual Setup
```bash
git clone <your-repo-url>
cd palmmind

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```



## 🔧 Environment Variables
Create `.env`:
```bash

DATABASE_URL=sqlite:///./rag_system.db
REDIS_HOST=localhost
REDIS_PORT=6379
QDRANT_URL=http://localhost:6333
LLM_MODEL=llama2
```

## 📚 API Overview
### 📄 Document Ingestion
POST /api/v1/documents/upload
- Upload and process PDF/TXT files into chunks + embeddings.

### 💬 Chat Query (RAG)
POST /api/v1/chat/query
- Ask a question and receive an AI-generated answer using document-based context + chat memory.

### 📅 Manual Interview Booking
POST /api/v1/chat/book-interview
- Submit structured booking details (name, email, date, time) directly for storage.
---

## 🏗️ Project Structure
```bash
palmmind/
  ├── app/
  │   ├── main.py              # 🚀 FastAPI entry point
  │   ├── api/                 # 🌐 API route handlers
  │   ├── models/              # 🗂️ Database models & schemas
  │   ├── services/            # 🧠 Core logic (RAG, embeddings, booking)
  │   └── utils/               # 🛠️ Utilities (chunking, file processing)
  ├── requirements.txt         # 📦 Python dependencies
  ├── docker-compose.yml       # 🐳 Multi-service setup (Redis, Qdrant, App)
  ├── Dockerfile               # 📄 App container build config
  └── README.md                # 📘 Project documentation
  ```

## 🐳 Docker Commands
```bash 
docker compose up --build
docker compose down
docker compose logs -f
docker compose ps
```


## 🚨 Troubleshooting

**1. Qdrant/Redis not connecting**  
- Ensure Docker is running  
- Run: docker compose restart  

**2. Document upload failing**  
- Ensure `uploads/` folder exists  
- Only PDF/TXT files allowed  

**3. API not responding**  
- Check logs: docker compose logs -f palmmind-app
