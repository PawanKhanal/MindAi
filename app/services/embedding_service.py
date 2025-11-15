import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import os
from typing import List, Dict, Any
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import re

class EmbeddingService:
    def __init__(self):
        self.vector_size = 300  # Fixed size for our embeddings
        self.vectorizer = None
        self.vocabulary = None
        
        self.qdrant_client = None
        self._initialize_qdrant()
    
    def _initialize_qdrant(self):
        """Initialize Qdrant client with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.qdrant_client = QdrantClient(
                    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
                    api_key=os.getenv("QDRANT_API_KEY", "")
                )
                
                self.qdrant_client.get_collections()
                print("✅ Successfully connected to Qdrant")
                
                self._ensure_collection_exists()
                break
                
            except Exception as e:
                print(f"❌ Qdrant connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("⚠️ Could not connect to Qdrant")
                    self.qdrant_client = None
    
    def _ensure_collection_exists(self):
        """Ensure the documents collection exists"""
        try:
            self.qdrant_client.get_collection("documents")
            print("✅ Documents collection exists")
        except Exception:
            print("📁 Creating documents collection...")
            self.qdrant_client.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            print("✅ Documents collection created")
    
    def _build_vocabulary(self, texts: List[str]):
        """Build a simple vocabulary for embeddings"""
        all_words = set()
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]{3,15}\b', text.lower())
            all_words.update(words)
        
        # Take top N most common words
        word_list = list(all_words)[:self.vector_size]
        self.vocabulary = {word: i for i, word in enumerate(word_list)}
        print(f"✅ Built vocabulary with {len(self.vocabulary)} words")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate simple word frequency based embeddings"""
        embeddings = []
        
        for text in texts:
            embedding = [0.0] * self.vector_size
            
            if self.vocabulary:
                # Word frequency based embedding
                words = re.findall(r'\b[a-zA-Z]{3,15}\b', text.lower())
                word_count = len(words)
                
                for word in words:
                    if word in self.vocabulary:
                        idx = self.vocabulary[word]
                        if idx < self.vector_size:
                            embedding[idx] += 1.0 / max(1, word_count)
            
            else:
                text_lower = text.lower()
                for i, char in enumerate(text_lower[:self.vector_size]):
                    if i < len(embedding):
                        embedding[i] = (ord(char) % 100) / 100.0
            
            # Normalize the embedding
            norm = max(0.001, np.linalg.norm(embedding))
            embedding = [x / norm for x in embedding]
            embeddings.append(embedding)
        
        return embeddings
    
    def store_embeddings(self, chunks: List[Dict[str, Any]], document_id: str) -> List[str]:
        """Store embeddings in Qdrant and return embedding IDs"""
        if self.qdrant_client is None:
            print("⚠️ Qdrant not available, skipping embedding storage")
            return [str(uuid.uuid4()) for _ in chunks]
        
        texts = [chunk["text"] for chunk in chunks]
        
        if self.vocabulary is None:
            self._build_vocabulary(texts)
        
        embeddings = self.generate_embeddings(texts)
        
        points = []
        embedding_ids = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            embedding_id = str(uuid.uuid4())
            embedding_ids.append(embedding_id)
            
            point = PointStruct(
                id=embedding_id,
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk["text"],
                    "chunk_metadata": chunk.get("chunk_metadata", {})
                }
            )
            points.append(point)
        
        try:
            self.qdrant_client.upsert(
                collection_name="documents",
                points=points
            )
            print(f"✅ Stored {len(points)} embeddings in Qdrant for document {document_id}")
        except Exception as e:
            print(f"❌ Failed to store embeddings in Qdrant: {e}")
        
        return embedding_ids
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if self.qdrant_client is None:
            print("⚠️ Qdrant not available, returning empty results")
            return []
        
        try:
            query_embedding = self.generate_embeddings([query])[0]
            
            search_results = self.qdrant_client.search(
                collection_name="documents",
                query_vector=query_embedding,
                limit=top_k
            )
            
            results = []
            for result in search_results:
                results.append({
                    "text": result.payload["text"],
                    "score": result.score,
                    "chunk_metadata": result.payload.get("chunk_metadata", {}),
                    "document_id": result.payload["document_id"]
                })
            
            print(f"✅ Found {len(results)} similar documents for query: '{query}'")
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []