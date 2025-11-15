from sqlalchemy import create_engine, Column, String, Text, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    chunking_strategy = Column(String)
    document_metadata = Column(JSON)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, index=True)
    chunk_text = Column(Text)
    chunk_index = Column(Integer) 
    chunk_metadata = Column(JSON) 
    embedding_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InterviewBooking(Base):
    __tablename__ = "interview_bookings"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    date = Column(String)
    time = Column(String)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag_system.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()