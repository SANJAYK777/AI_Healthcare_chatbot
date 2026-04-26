"""
BioBERT Service - Medical Entity Recognition and Symptom Analysis
"""
from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class BioBERTService:
    """Service for medical entity recognition using BioBERT"""
    
    def __init__(self, model_name: str = "dmis-lab/biobert-base-cased-v1.1"):
        """
        Initialize BioBERT service
        Args:
            model_name: BioBERT model to use
        """
        self.model_name = model_name
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            logger.info(f"✓ BioBERT loaded: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load BioBERT: {str(e)}")
            self.tokenizer = None
            self.model = None
    
    def extract_medical_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract medical entities from text
        This is a simplified version - full NER would need a trained NER head
        """
        if not self.tokenizer or not self.model:
            return []
        
        try:
            inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model(**inputs)
            
            # Get embeddings for semantic understanding
            # In production, this would use a fine-tuned NER head
            return self._extract_entities_from_text(text)
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return []
    
    def _extract_entities_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Simple pattern-based entity extraction
        In production, use a fine-tuned BioBERT-NER model
        """
        entities = []
        
        # Medical entities and conditions
        medical_terms = {
            "SYMPTOM": ["fever", "cough", "headache", "nausea", "fatigue", 
                       "sore throat", "pain", "ache", "swelling", "rash"],
            "CONDITION": ["diabetes", "hypertension", "asthma", "bronchitis", 
                         "pneumonia", "flu", "covid", "arthritis", "anxiety"],
            "TREATMENT": ["medication", "antibiotics", "rest", "hydration", 
                         "exercise", "therapy", "surgery"],
            "BODY_PART": ["throat", "chest", "head", "stomach", "back", 
                         "knee", "heart", "lung", "liver", "kidney"]
        }
        
        text_lower = text.lower()
        
        for entity_type, terms in medical_terms.items():
            for term in terms:
                if term in text_lower:
                    start_pos = text_lower.find(term)
                    if start_pos != -1:
                        entities.append({
                            "text": term,
                            "type": entity_type,
                            "start": start_pos,
                            "end": start_pos + len(term)
                        })
        
        return entities
    
    def predict_conditions(self, symptoms: List[str]) -> List[Tuple[str, float]]:
        """
        Predict possible medical conditions from symptoms
        Returns list of (condition, confidence) tuples
        """
        # Symptom-condition mapping (simplified)
        condition_mapping = {
            "Common Cold": ["cough", "sore throat", "runny nose", "fatigue"],
            "Flu": ["fever", "cough", "body aches", "fatigue"],
            "Bronchitis": ["persistent cough", "chest discomfort", "fever"],
            "Asthma": ["wheezing", "shortness of breath", "chest tightness"],
            "Allergies": ["sneezing", "itchy eyes", "runny nose", "rash"],
            "Headache": ["head pain", "tension", "sensitivity to light"],
            "Gastroenteritis": ["nausea", "vomiting", "diarrhea", "stomach pain"],
            "Anxiety": ["nervousness", "heart palpitations", "breathing difficulty"],
        }
        
        predictions = []
        symptoms_lower = [s.lower() for s in symptoms]
        
        for condition, condition_symptoms in condition_mapping.items():
            # Calculate matching score
            matches = sum(1 for sym in condition_symptoms 
                         if any(sym_key in symp for sym_key in symptoms_lower 
                               for symp in [sym_key]))
            
            if matches > 0:
                confidence = min(matches / len(condition_symptoms), 1.0)
                predictions.append((condition, confidence))
        
        # Sort by confidence
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:3]  # Return top 3


def get_biobert_service() -> BioBERTService:
    """Factory function to create BioBERT service"""
    return BioBERTService()
