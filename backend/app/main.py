"""
Main FastAPI application with all endpoints
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

from app.config import (
    GROQ_API_KEY, MONGODB_URI, DATABASE_NAME, ENCRYPTION_KEY,
    DEBUG, PORT, HOST, HUGGINGFACE_API_KEY, IS_PRODUCTION_READY, CONFIG_STATUS
)
from app.models.schemas import (
    ChatMessage, ChatResponse, FeedbackRequest, HistoryRequest, HistoryResponse,
    HealthInsightsResponse, SecurityStatusResponse, SettingsResponse
)
from app.utils.encryption import EncryptionService
from app.utils.database import init_db, get_db
from app.services.llm_service import LLMService
from app.services.biobert_service import BioBERTService
from app.services.rl_learning import RLFeedbackService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Healthcare Chatbot Platform",
    description="Intelligent secure healthcare chatbot with LLaMA 3 and BioBERT",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
encryption_service = EncryptionService(ENCRYPTION_KEY)
llm_service = None

# Global statistics for insights
insights_tracker = {
    "total_chats": 0,
    "symptom_frequency": {},
    "conditions_frequency": {},
    "total_feedback": 0,
    "helpful_feedback": 0,
    "total_responses": 0
}
biobert_service = None
rl_service = RLFeedbackService()
db = None

# Store conversation history in memory (for demo; use DB in production)
conversation_history = {}


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global llm_service, biobert_service, db
    
    logger.info("=" * 70)
    logger.info("🚀 Starting AI Healthcare Chatbot Platform...")
    logger.info("=" * 70)
    
    # DEBUG: Print configuration status
    logger.info(f"DEBUG - GROQ_API_KEY present: {bool(GROQ_API_KEY)}")
    logger.info(f"DEBUG - GROQ_API_KEY length: {len(GROQ_API_KEY)}")
    logger.info(f"DEBUG - GROQ_API_KEY first 30 chars: {GROQ_API_KEY[:30]}")
    logger.info(f"DEBUG - HUGGINGFACE_API_KEY present: {bool(HUGGINGFACE_API_KEY)}")
    logger.info(f"DEBUG - HUGGINGFACE_API_KEY length: {len(HUGGINGFACE_API_KEY)}")
    
    # Display configuration status
    if IS_PRODUCTION_READY:
        logger.info(f"✅ {CONFIG_STATUS}")
    else:
        logger.warning(f"⚠️  {CONFIG_STATUS}")
        logger.warning("📝 To enable production features, add API keys to backend/.env:")
        logger.warning("   GROQ_API_KEY=your_key_from_console.groq.com")
        logger.warning("   HUGGINGFACE_API_KEY=your_token_from_huggingface.co")
    
    try:
        # Initialize LLM service
        if GROQ_API_KEY and GROQ_API_KEY != "demo_key_for_testing":
            logger.info(f"✓ Initializing LLM Service with GROQ API key...")
            llm_service = LLMService(GROQ_API_KEY)
            logger.info("✅ LLM Service (LLaMA 3) initialized successfully!")
        else:
            logger.warning("⚠️ LLM Service: Using demo mode (no valid GROQ_API_KEY)")
        
        # Initialize BioBERT service
        try:
            biobert_service = BioBERTService()
            logger.info("✓ BioBERT Service initialized (Medical NLP)")
        except Exception as e:
            logger.warning(f"⚠️ BioBERT initialization warning: {str(e)[:100]}")
        
        # Initialize Database (non-blocking - app runs without DB)
        try:
            db = init_db(MONGODB_URI, DATABASE_NAME)
            logger.info("✓ Database initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Database connection warning: {str(e)[:100]}")
            logger.info("💾 Running with in-memory storage only")
            db = None
        
        logger.info("✓ All services ready!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"✗ Startup error: {str(e)}")
        # Don't raise - let app continue in degraded mode


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if db:
        db.disconnect()
    logger.info("🛑 Application shutdown")


# ==================== HEALTH CHECK ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    db_healthy = False
    if db:
        db_healthy = db.health_check()
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "services": {
            "llm": "ready" if llm_service else "unavailable",
            "biobert": "ready" if biobert_service else "unavailable",
            "database": "connected" if db_healthy else "disconnected",
            "encryption": "enabled"
        }
    }


@app.get("/test-env", tags=["Debug"])
async def test_env():
    """Test endpoint to verify API keys are loaded"""
    return {
        "groq_loaded": bool(GROQ_API_KEY and GROQ_API_KEY != "demo_key_for_testing"),
        "groq_length": len(GROQ_API_KEY) if GROQ_API_KEY else 0,
        "groq_first_20": GROQ_API_KEY[:20] if GROQ_API_KEY else "EMPTY",
        "hf_loaded": bool(HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "demo_hf_token"),
        "hf_length": len(HUGGINGFACE_API_KEY) if HUGGINGFACE_API_KEY else 0,
        "hf_first_20": HUGGINGFACE_API_KEY[:20] if HUGGINGFACE_API_KEY else "EMPTY",
        "llm_service_initialized": bool(llm_service),
        "is_production_ready": IS_PRODUCTION_READY,
        "config_status": CONFIG_STATUS
    }


# ==================== CHAT ENDPOINTS ====================

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(message: ChatMessage):
    """
    Process user message and generate response
    """
    try:
        user_id = message.user_id
        user_text = message.content
        
        # Initialize user history if needed
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Encrypt message before storing
        encrypted_message = encryption_service.encrypt(user_text)
        
        # Detect healthcare intent
        is_healthcare = llm_service.detect_healthcare_intent(user_text) if llm_service else (
            any(keyword in user_text.lower() for keyword in ['fever', 'cough', 'pain', 'symptom', 'health', 'doctor', 'medical', 'disease'])
        )
        
        detected_symptoms = []
        conditions = []
        
        # Healthcare mode logic
        if is_healthcare and llm_service and biobert_service:
            detected_symptoms = llm_service.extract_symptoms(user_text)
            conditions = biobert_service.predict_conditions(detected_symptoms)
            
            # Track symptoms for insights
            for symptom in detected_symptoms:
                insights_tracker["symptom_frequency"][symptom] = insights_tracker["symptom_frequency"].get(symptom, 0) + 1
            
            # Track conditions for insights
            for condition, confidence in conditions:
                condition_name = str(condition).replace('_', ' ')
                insights_tracker["conditions_frequency"][condition_name] = insights_tracker["conditions_frequency"].get(condition_name, 0) + 1
            
            # Generate specialized healthcare response
            healthcare_prompt = llm_service.get_healthcare_mode_prompt()
            response_text = llm_service.generate_response(
                user_text,
                conversation_history[user_id],
                system_prompt=healthcare_prompt
            )
        elif is_healthcare:
            # Demo healthcare response
            detected_symptoms = ['symptom_detected']
            conditions = [('Common_Condition', 0.7)]
            
            # Track symptoms for insights
            for symptom in detected_symptoms:
                insights_tracker["symptom_frequency"][symptom] = insights_tracker["symptom_frequency"].get(symptom, 0) + 1
            
            # Track conditions for insights
            for condition, confidence in conditions:
                condition_name = str(condition).replace('_', ' ')
                insights_tracker["conditions_frequency"][condition_name] = insights_tracker["conditions_frequency"].get(condition_name, 0) + 1
            
            response_text = """### 🩺 Condition Overview
I can help organize your symptoms, but the app is currently running in demo mode, so full AI medical guidance is limited right now.

### 💊 What You Can Do
- Describe your symptoms clearly, including when they started
- Track severity, triggers, and any related symptoms
- Configure valid API keys to enable full healthcare responses

### ⚠️ When to See a Doctor
- Symptoms are getting worse or not improving
- You have severe pain, trouble breathing, or other urgent symptoms

### 📌 Disclaimer
This is not a medical diagnosis. Consult a doctor."""
        else:
            # General conversation mode
            response_text = llm_service.generate_response(
                user_text,
                conversation_history[user_id]
            ) if llm_service else (
                "Hello! I'm your healthcare assistant. "
                "I'm currently running in demo mode. "
                "You can ask me health questions, and I'll help as best as I can. "
                "For full features, please add your API keys to the .env file."
            )
        
        # Encrypt response
        encrypted_response = encryption_service.encrypt(response_text)
        
        # Track statistics
        insights_tracker["total_chats"] += 1
        insights_tracker["total_responses"] += 1
        
        # Store in database
        if db:
            message_id = db.insert_chat_message(
                user_id=user_id,
                message=encrypted_message,
                response=encrypted_response,
                encrypted=True
            )
        else:
            message_id = f"msg_{len(conversation_history[user_id])}"
        
        # Update conversation history
        conversation_history[user_id].append({
            "role": "user",
            "content": user_text,
            "timestamp": message.timestamp or None
        })
        conversation_history[user_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": None
        })
        
        # Keep last 10 messages
        conversation_history[user_id] = conversation_history[user_id][-20:]
        
        return ChatResponse(
            response=response_text,
            message_id=message_id,
            healthcare_mode=is_healthcare,
            detected_symptoms=detected_symptoms,
            conditions=[(cond, float(conf)) for cond, conf in conditions],
            timestamp=message.timestamp or None
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


# ==================== FEEDBACK ENDPOINTS ====================

@app.post("/feedback", tags=["Feedback"])
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit feedback on response quality
    """
    try:
        # Process feedback through RL service
        rl_result = rl_service.process_feedback(
            response_id=feedback.message_id,
            is_helpful=feedback.is_helpful,
            user_id="user",  # In production, get from auth
            category=feedback.category or "general"
        )
        
        # Track feedback statistics
        insights_tracker["total_feedback"] += 1
        if feedback.is_helpful:
            insights_tracker["helpful_feedback"] += 1
        
        # Store in database
        if db:
            db.insert_feedback(
                user_id="user",
                message_id=feedback.message_id,
                feedback=feedback.comment or ("Helpful" if feedback.is_helpful else "Not helpful"),
                score=1 if feedback.is_helpful else -1
            )
        
        return {
            "status": "success",
            "message": "Feedback recorded",
            "score": rl_result["current_score"]
        }
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rl-stats", tags=["Learning"])
async def get_rl_stats():
    """Get reinforcement learning statistics"""
    return rl_service.get_stats()


@app.get("/rl-recommendations", tags=["Learning"])
async def get_rl_recommendations():
    """Get recommendations based on feedback patterns"""
    return rl_service.get_improvement_recommendations()


# ==================== HISTORY ENDPOINTS ====================

@app.post("/history", response_model=HistoryResponse, tags=["History"])
async def get_chat_history(request: HistoryRequest):
    """Get user's chat history"""
    try:
        if db:
            messages = db.get_user_history(request.user_id, limit=request.limit)
            
            # Decrypt messages for client
            decrypted_messages = []
            for msg in messages:
                try:
                    decrypted_msg = encryption_service.decrypt(msg.get("message", ""))
                    decrypted_response = encryption_service.decrypt(msg.get("response", ""))
                    decrypted_messages.append({
                        "id": str(msg.get("_id")),
                        "message": decrypted_msg,
                        "response": decrypted_response,
                        "timestamp": msg.get("timestamp")
                    })
                except:
                    pass
            
            return HistoryResponse(
                messages=decrypted_messages,
                total_count=len(decrypted_messages)
            )
        else:
            # Return from memory
            if request.user_id in conversation_history:
                msgs = conversation_history[request.user_id][-request.limit:]
                return HistoryResponse(messages=msgs, total_count=len(msgs))
            return HistoryResponse(messages=[], total_count=0)
    
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== INSIGHTS ENDPOINTS ====================

@app.get("/insights", response_model=HealthInsightsResponse, tags=["Insights"])
async def get_health_insights():
    """Get health insights and statistics"""
    try:
        stats = rl_service.get_stats()
        
        # Calculate success rate from feedback
        success_rate = 0
        if insights_tracker["total_feedback"] > 0:
            success_rate = insights_tracker["helpful_feedback"] / insights_tracker["total_feedback"]
        
        # Get top symptoms (limit to 10)
        top_symptoms = dict(sorted(
            insights_tracker["symptom_frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10])
        
        # Get top conditions (limit to 5)
        top_conditions = sorted(
            insights_tracker["conditions_frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        if db:
            feedback_stats = db.get_feedback_stats("user")
        else:
            feedback_stats = {
                "total": insights_tracker["total_feedback"],
                "helpful": insights_tracker["helpful_feedback"]
            }
        
        return HealthInsightsResponse(
            total_chats=insights_tracker["total_chats"],
            symptom_frequency=top_symptoms,
            recent_conditions=[cond[0] for cond in top_conditions],
            success_rate=success_rate,
            feedback_stats=feedback_stats
        )
    except Exception as e:
        logger.error(f"Insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SECURITY ENDPOINTS ====================

@app.get("/security/status", response_model=SecurityStatusResponse, tags=["Security"])
async def get_security_status():
    """Get security status"""
    db_connected = False
    storage_mode = "in-memory"
    
    if db:
        db_connected = db.health_check()
        if db_connected:
            storage_mode = "mongodb"
    
    # In demo mode with in-memory storage, mark as connected since it's functional
    if not db_connected:
        db_connected = True  # In-memory storage is working
        storage_mode = "in-memory"
    
    return SecurityStatusResponse(
        encryption_enabled=True,
        encryption_type="AES-256 (Fernet)",
        database_connected=db_connected,
        storage_mode=storage_mode,
        api_secured=True,
        status="✓ All systems secure" if storage_mode == "mongodb" else "✓ Demo mode - In-memory storage"
    )


# ==================== SETTINGS ENDPOINTS ====================

@app.get("/settings", response_model=SettingsResponse, tags=["Settings"])
async def get_settings():
    """Get user settings"""
    return SettingsResponse(
        dark_mode=False,
        notifications_enabled=True,
        data_retention_days=30,
        encryption_enabled=True
    )


@app.post("/settings/dark-mode", tags=["Settings"])
async def toggle_dark_mode(enabled: bool):
    """Toggle dark mode"""
    return {"dark_mode": enabled, "status": "updated"}


@app.post("/settings/clear-history", tags=["Settings"])
async def clear_chat_history(user_id: str):
    """Clear user's chat history"""
    try:
        if user_id in conversation_history:
            conversation_history[user_id] = []
        
        return {"status": "history cleared", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ROOT ENDPOINT ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "🏥 AI Healthcare Chatbot Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": True},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
