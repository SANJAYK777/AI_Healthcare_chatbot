"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message model"""
    content: str = Field(..., min_length=1, max_length=5000)
    user_id: str
    timestamp: Optional[datetime] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    message_id: str
    healthcare_mode: bool
    detected_symptoms: List[str] = []
    conditions: List[tuple] = []
    timestamp: Optional[datetime] = None


class FeedbackRequest(BaseModel):
    """Feedback request model"""
    message_id: str
    is_helpful: bool
    category: Optional[str] = "general"
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Feedback response model"""
    status: str
    message: str
    score: float


class HistoryRequest(BaseModel):
    """History request model"""
    user_id: str
    limit: Optional[int] = 50


class HistoryResponse(BaseModel):
    """History response model"""
    messages: List[dict]
    total_count: int


class HealthInsightsResponse(BaseModel):
    """Health insights response"""
    total_chats: int
    symptom_frequency: dict
    recent_conditions: List[str]
    success_rate: float
    feedback_stats: dict


class SecurityStatusResponse(BaseModel):
    """Security status response"""
    encryption_enabled: bool
    encryption_type: str
    database_connected: bool
    storage_mode: str  # 'mongodb' or 'in-memory'
    api_secured: bool
    status: str


class SettingsResponse(BaseModel):
    """Settings response"""
    dark_mode: bool
    notifications_enabled: bool
    data_retention_days: int
    encryption_enabled: bool
