import PyPDF2
import os
from typing import Tuple
import uuid

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error extracting text from TXT file: {str(e)}")

def save_uploaded_file(file_content: bytes, filename: str) -> Tuple[str, str]:
    """Save uploaded file and return file path"""
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1].lower()
    upload_dir = "uploads"
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, f"{file_id}{file_extension}")
    
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    return file_path, file_id