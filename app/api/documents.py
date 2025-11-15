from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os

from app.models.schemas import DocumentResponse, ChunkingStrategy
from app.services.document_ingestion import DocumentIngestionService

router = APIRouter()
ingestion_service = DocumentIngestionService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Form(default=ChunkingStrategy.FIXED_SIZE)
):
    """Upload and process document"""
    
    # Validate file type
    allowed_extensions = {'.pdf', '.txt'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    try:
        file_content = await file.read()
        
        result = await ingestion_service.process_document(
            file_content, 
            file.filename, 
            chunking_strategy.value
        )
        
        return DocumentResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        await file.close()