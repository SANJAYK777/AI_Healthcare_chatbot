"""
Configuration file for the AI Healthcare Chatbot
Loads and validates environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get absolute path to .env file
ENV_FILE = Path(__file__).parent.parent / ".env"
print(f"🔍 Loading .env from: {ENV_FILE}")
print(f"🔍 .env exists: {ENV_FILE.exists()}")

# Load environment variables from .env file using absolute path
load_dotenv(dotenv_path=str(ENV_FILE), override=True)

# ==================== API KEYS ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://demo:demo@test.mongodb.net/healthcare")

# DEBUG: Print loaded keys (first 20 chars for security)
print(f"✓ CONFIG LOADED - GROQ_API_KEY (first 20 chars): {GROQ_API_KEY[:20] if GROQ_API_KEY else 'EMPTY'}")
print(f"✓ CONFIG LOADED - HUGGINGFACE_API_KEY (first 20 chars): {HUGGINGFACE_API_KEY[:20] if HUGGINGFACE_API_KEY else 'EMPTY'}")
print(f"✓ CONFIG LOADED - GROQ_API_KEY length: {len(GROQ_API_KEY)}")
print(f"✓ CONFIG LOADED - HUGGINGFACE_API_KEY length: {len(HUGGINGFACE_API_KEY)}")

# Encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")

# ==================== MODEL CONFIGURATION ====================
LLAMA_MODEL = "llama-3.1-8b-instant"  # Groq's fast Llama model
BIOBERT_MODEL = "dmis-lab/biobert-base-cased-v1.1"

# ==================== SERVER CONFIGURATION ====================
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")
DATABASE_NAME = os.getenv("DATABASE_NAME", "healthcare")

# ==================== CORS CONFIGURATION ====================
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:5173",
]

# ==================== VALIDATION & STATUS ====================
def validate_configuration():
    """
    Validate that all required configurations are properly set.
    Returns (is_production_ready, status_message)
    """
    missing_keys = []
    
    # Check for demo/placeholder values
    if not GROQ_API_KEY or GROQ_API_KEY == "demo_key_for_testing":
        missing_keys.append("GROQ_API_KEY")
    
    if not HUGGINGFACE_API_KEY or HUGGINGFACE_API_KEY == "demo_hf_token":
        missing_keys.append("HUGGINGFACE_API_KEY")
    
    if missing_keys:
        return False, f"Missing or invalid API keys: {', '.join(missing_keys)}"
    
    return True, "All API keys configured - Production mode enabled!"

# Get configuration status
IS_PRODUCTION_READY, CONFIG_STATUS = validate_configuration()

# Database
DATABASE_NAME = "healthcare_chatbot"
COLLECTIONS = {
    "users": "users",
    "chat_history": "chat_history",
    "feedback": "feedback",
    "sessions": "sessions"
}

# Server
DEBUG = os.getenv("DEBUG", "True") == "True"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
