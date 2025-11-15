import uuid
from typing import Any
import os

from app.utils.file_processing import extract_text_from_pdf, extract_text_from_txt, save_uploaded_file
from app.utils.chunking import get_chunking_strategy
from app.services.embedding_service import EmbeddingService
from app.models.database import get_db, Document, DocumentChunk

class DocumentIngestionService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    async def process_document(self, file_content: bytes, filename: str, chunking_strategy: str) -> dict[str, Any]:
        """Process uploaded document"""
        
        file_path, file_id = save_uploaded_file(file_content, filename)
        
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_extension == '.txt':
            text = extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        chunking_fn = get_chunking_strategy(chunking_strategy)
        chunks = chunking_fn(text)
        
        embedding_ids = self.embedding_service.store_embeddings(chunks, file_id)
        
        db = get_db()
        try:
            document = Document(
                id=file_id,
                filename=filename,
                file_path=file_path,
                chunking_strategy=chunking_strategy,
                document_metadata={"chunk_count": len(chunks), "file_size": len(file_content)} 
            )
            db.add(document)
            
            for i, (chunk, embedding_id) in enumerate(zip(chunks, embedding_ids)):
                chunk_record = DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=file_id,
                    chunk_text=chunk["text"][:1000],  # Store truncated text for reference
                    chunk_index=i, 
                    chunk_metadata={  
                        **chunk.get("chunk_metadata", {}),
                        "embedding_id": embedding_id,
                        "text_length": len(chunk["text"])
                    },
                    embedding_id=embedding_id
                )
                db.add(chunk_record)
            
            db.commit()
            
            return {
                "document_id": file_id,
                "filename": filename,
                "chunk_count": len(chunks),
                "status": "processed"
            }
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()