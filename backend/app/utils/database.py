"""
MongoDB Database Connection and Operations
"""
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """Manages MongoDB connections and operations"""
    
    def __init__(self, mongodb_uri: str, database_name: str):
        """
        Initialize database service
        Args:
            mongodb_uri: MongoDB connection string
            database_name: Database name
        """
        self.mongodb_uri = mongodb_uri
        self.database_name = database_name
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database_name]
            # Test connection
            self.db.command("ping")
            logger.info("✓ Connected to MongoDB")
            return True
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.error(f"✗ MongoDB connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB disconnected")
    
    def insert_chat_message(self, user_id: str, message: str, response: str, 
                           encrypted: bool = True) -> str:
        """Store chat message and response"""
        chat_data = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "encrypted": encrypted,
            "timestamp": datetime.utcnow(),
            "feedback": None
        }
        result = self.db.chat_history.insert_one(chat_data)
        return str(result.inserted_id)
    
    def insert_feedback(self, user_id: str, message_id: str, 
                       feedback: str, score: int) -> bool:
        """Store user feedback for learning"""
        feedback_data = {
            "user_id": user_id,
            "message_id": message_id,
            "feedback": feedback,
            "score": score,  # 1 for helpful, -1 for not helpful
            "timestamp": datetime.utcnow()
        }
        self.db.feedback.insert_one(feedback_data)
        
        # Update message with feedback
        self.db.chat_history.update_one(
            {"_id": message_id},
            {"$set": {"feedback": feedback, "score": score}}
        )
        return True
    
    def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve user chat history"""
        messages = list(self.db.chat_history.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit))
        return messages
    
    def get_feedback_stats(self, user_id: str) -> Dict[str, Any]:
        """Get feedback statistics for learning"""
        feedback = list(self.db.feedback.find({"user_id": user_id}))
        total = len(feedback)
        helpful = sum(1 for f in feedback if f.get("score", 0) > 0)
        not_helpful = total - helpful
        
        return {
            "total_feedback": total,
            "helpful": helpful,
            "not_helpful": not_helpful,
            "success_rate": (helpful / total * 100) if total > 0 else 0
        }
    
    def create_session(self, user_id: str, session_data: Dict) -> str:
        """Create a new session"""
        session = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            **session_data
        }
        result = self.db.sessions.insert_one(session)
        return str(result.inserted_id)
    
    def health_check(self) -> bool:
        """Check database connection health"""
        try:
            self.db.command("ping")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


# Global database instance
_db_service: Optional[DatabaseService] = None


def init_db(mongodb_uri: str, database_name: str) -> DatabaseService:
    """Initialize database service"""
    global _db_service
    _db_service = DatabaseService(mongodb_uri, database_name)
    _db_service.connect()
    return _db_service


def get_db() -> DatabaseService:
    """Get database service instance"""
    if _db_service is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db_service
