"""
LLM Service - Handles LLaMA 3 integration via Groq API
"""
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLaMA 3 via Groq"""

    def __init__(self, api_key: str, model_name: str = "llama-3.1-8b-instant"):
        """
        Initialize LLM service
        Args:
            api_key: Groq API key
            model_name: Model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.chat = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.7,
            max_tokens=1024
        )
        self.system_prompt = """You are a compassionate and knowledgeable healthcare assistant AI.

Your responsibilities:
1. Listen carefully to user symptoms and concerns
2. Ask thoughtful follow-up questions when needed
3. Provide evidence-based general health information
4. NEVER provide medical diagnoses - only suggestions
5. Always recommend consulting a healthcare provider
6. Show empathy and understanding
7. Be professional but friendly

CRITICAL DISCLAIMER for every response when discussing health:
"Disclaimer: This is not a medical diagnosis. For accurate diagnosis and treatment, please consult a qualified healthcare provider."

Keep responses concise but helpful."""
        self.healthcare_system_prompt = """You are a healthcare AI assistant.

You MUST follow this response format EXACTLY.

Do NOT write paragraphs.

ONLY use this structure:

### 🩺 Condition Overview
- Write 1-2 short bullet points

### 💊 What You Should Do
- Action 1
- Action 2
- Action 3

### ⚠️ When to See a Doctor
- Warning 1
- Warning 2

### 📌 Disclaimer
- This is not a medical diagnosis. Consult a doctor.

RULES:
- Use ONLY bullet points
- Each line MUST start with "-"
- NO long paragraphs
- NO numbering (1,2,3)
- Keep answers short and clean
- Do not provide a definitive diagnosis"""

    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a response using LLaMA 3
        Args:
            user_message: User's input message
            conversation_history: Previous messages for context
            system_prompt: Optional system prompt override
        Returns:
            Generated response
        """
        try:
            active_system_prompt = system_prompt or self.system_prompt
            messages = [SystemMessage(content=active_system_prompt)]

            if conversation_history:
                for msg in conversation_history[-5:]:
                    if msg.get("role") == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    else:
                        messages.append(SystemMessage(content=msg["content"]))

            messages.append(HumanMessage(content=user_message))

            response = self.chat.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            return "I'm having trouble processing your request. Please try again."

    def detect_healthcare_intent(self, user_message: str) -> bool:
        """
        Detect if the message contains healthcare-related intent
        Args:
            user_message: User's input
        Returns:
            True if healthcare-related, False otherwise
        """
        healthcare_keywords = [
            "symptom", "pain", "sick", "disease", "condition", "treatment",
            "medicine", "doctor", "health", "illness", "fever", "cough",
            "headache", "nausea", "fatigue", "injured", "hurt", "ache",
            "diagnose", "prescription", "hospital", "emergency", "allergy",
            "infection", "swollen", "bleeding", "dizzy", "weak"
        ]

        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in healthcare_keywords)

    def get_healthcare_mode_prompt(self) -> str:
        """Get prompt for healthcare specialist mode"""
        return self.healthcare_system_prompt

    def extract_symptoms(self, message: str) -> List[str]:
        """
        Extract symptoms from user message (simple pattern matching)
        This would be enhanced with BioBERT in production
        """
        symptom_patterns = {
            "fever": ["fever", "high temperature", "temp", "hot"],
            "cough": ["cough", "coughing", "dry cough", "persistent cough"],
            "headache": ["headache", "head pain", "migraine", "head ache"],
            "nausea": ["nausea", "feeling sick", "queasy", "sick stomach"],
            "fatigue": ["fatigue", "tired", "exhausted", "no energy", "weak"],
            "sore throat": ["sore throat", "throat pain", "throat hurts"],
            "body aches": ["body aches", "muscle pain", "joint pain", "aching"],
        }

        detected_symptoms = []
        message_lower = message.lower()

        for symptom, patterns in symptom_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                detected_symptoms.append(symptom)

        return detected_symptoms


def get_llm_service(api_key: str) -> LLMService:
    """Factory function to create LLM service"""
    return LLMService(api_key)
