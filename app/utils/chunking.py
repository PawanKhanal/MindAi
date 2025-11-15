from typing import List, Dict, Any
import re

class ChunkingStrategy:
    @staticmethod
    def fixed_size_chunking(text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
        """Fixed size chunking strategy without LangChain"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            
            if current_size + word_size > chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append({"text": chunk_text, "metadata": {}})
                
                # Start new chunk with overlap
                overlap_words = current_chunk[-chunk_overlap:] if chunk_overlap > 0 else []
                current_chunk = overlap_words + [word]
                current_size = sum(len(w) + 1 for w in current_chunk)
            else:
                current_chunk.append(word)
                current_size += word_size
        
        # Add the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({"text": chunk_text, "metadata": {}})
        
        return chunks
    
    @staticmethod
    def semantic_chunking(text: str, chunk_size: int = 512) -> List[Dict[str, Any]]:
        """Semantic chunking using sentence boundaries"""
        # Split by sentences (simple approach)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > chunk_size and current_chunk:
                # Save current chunk
                chunk_text = '. '.join(current_chunk) + '.'
                chunks.append({"text": chunk_text, "metadata": {}})
                
                # Start new chunk
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        # Add the last chunk
        if current_chunk:
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append({"text": chunk_text, "metadata": {}})
        
        return chunks

def get_chunking_strategy(strategy: str):
    """Get the appropriate chunking strategy"""
    strategies = {
        "fixed_size": ChunkingStrategy.fixed_size_chunking,
        "semantic": ChunkingStrategy.semantic_chunking
    }
    return strategies.get(strategy, ChunkingStrategy.fixed_size_chunking)