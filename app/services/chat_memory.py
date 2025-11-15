import redis
import json
import os
from typing import List, Dict, Any

class ChatMemory:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )
    
    def add_message(self, session_id: str, message: Dict[str, str]):
        """Add message to chat history"""
        key = f"chat_session:{session_id}"
        self.redis_client.rpush(key, json.dumps(message))
        self.redis_client.expire(key, 3600)  # Expire after 1 hour
    
    def get_messages(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get chat history for session"""
        key = f"chat_session:{session_id}"
        messages = self.redis_client.lrange(key, -limit, -1)
        return [json.loads(msg) for msg in messages]
    
    def clear_messages(self, session_id: str):
        """Clear chat history for session"""
        key = f"chat_session:{session_id}"
        self.redis_client.delete(key)