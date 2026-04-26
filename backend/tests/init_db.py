"""
Database initialization script
Initializes MongoDB collections and indexes
"""
import os
from dotenv import load_dotenv
from app.utils.database import DatabaseService

load_dotenv()

def init_database():
    """Initialize database with collections and indexes"""
    
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME", "healthcare_chatbot")
    
    if not mongodb_uri:
        print("✗ MONGODB_URI not found in .env")
        return False
    
    print("🔌 Initializing database...")
    
    db = DatabaseService(mongodb_uri, database_name)
    if not db.connect():
        print("✗ Failed to connect to MongoDB")
        return False
    
    try:
        # Create collections with validation
        collections = db.db.list_collection_names()
        
        # Chat History Collection
        if "chat_history" not in collections:
            print("Creating chat_history collection...")
            db.db.create_collection("chat_history")
            db.db.chat_history.create_index([("user_id", 1), ("timestamp", -1)])
            db.db.chat_history.create_index([("encrypted", 1)])
            print("✓ chat_history collection created")
        
        # Feedback Collection
        if "feedback" not in collections:
            print("Creating feedback collection...")
            db.db.create_collection("feedback")
            db.db.feedback.create_index([("user_id", 1), ("timestamp", -1)])
            db.db.feedback.create_index([("message_id", 1)])
            print("✓ feedback collection created")
        
        # Sessions Collection
        if "sessions" not in collections:
            print("Creating sessions collection...")
            db.db.create_collection("sessions")
            db.db.sessions.create_index([("user_id", 1)])
            db.db.sessions.create_index([("created_at", 1)])
            print("✓ sessions collection created")
        
        # Users Collection
        if "users" not in collections:
            print("Creating users collection...")
            db.db.create_collection("users")
            db.db.users.create_index([("user_id", 1)], unique=True)
            print("✓ users collection created")
        
        # Insert sample data
        print("\nInserting sample data...")
        sample_user = {
            "user_id": "demo_user",
            "created_at": db.db.chat_history.find_one() is None,
            "preferences": {
                "dark_mode": False,
                "notifications": True,
                "data_retention_days": 30
            }
        }
        db.db.users.insert_one(sample_user)
        print("✓ Sample user created")
        
        db.disconnect()
        print("\n✓ Database initialization complete!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        db.disconnect()
        return False

if __name__ == "__main__":
    init_database()
