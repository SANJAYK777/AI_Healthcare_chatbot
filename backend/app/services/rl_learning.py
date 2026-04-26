"""
Reinforcement Learning Service - Learns from user feedback
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RLFeedbackService:
    """
    Reinforcement Learning system that learns from user feedback
    Maintains a scoring system for response quality improvement
    """
    
    def __init__(self):
        """Initialize RL service"""
        self.response_scores: Dict[str, List[int]] = {}
        self.feedback_history: List[Dict] = []
    
    def process_feedback(self, response_id: str, is_helpful: bool, 
                        user_id: str, category: str = "general") -> Dict:
        """
        Process user feedback and update scoring
        Args:
            response_id: ID of the response being rated
            is_helpful: True if helpful, False if not
            user_id: ID of the user providing feedback
            category: Category of response (general, healthcare, etc)
        Returns:
            Updated scoring data
        """
        score = 1 if is_helpful else -1
        
        if response_id not in self.response_scores:
            self.response_scores[response_id] = []
        
        self.response_scores[response_id].append(score)
        
        feedback_entry = {
            "response_id": response_id,
            "user_id": user_id,
            "helpful": is_helpful,
            "score": score,
            "category": category,
            "timestamp": datetime.utcnow()
        }
        self.feedback_history.append(feedback_entry)
        
        logger.info(f"Feedback received for {response_id}: {'helpful' if is_helpful else 'not helpful'}")
        
        return {
            "status": "processed",
            "response_id": response_id,
            "current_score": self.get_response_score(response_id)
        }
    
    def get_response_score(self, response_id: str) -> float:
        """
        Calculate average score for a response
        Returns value between -1 and 1
        """
        if response_id not in self.response_scores:
            return 0.0
        
        scores = self.response_scores[response_id]
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_category_performance(self, category: str) -> Dict:
        """Get performance metrics for a category"""
        category_feedback = [f for f in self.feedback_history 
                            if f["category"] == category]
        
        if not category_feedback:
            return {"category": category, "total": 0}
        
        helpful = sum(1 for f in category_feedback if f["helpful"])
        total = len(category_feedback)
        
        return {
            "category": category,
            "total_responses": total,
            "helpful": helpful,
            "not_helpful": total - helpful,
            "success_rate": (helpful / total * 100) if total > 0 else 0
        }
    
    def get_user_performance(self, user_id: str) -> Dict:
        """Get performance metrics for a user's interactions"""
        user_feedback = [f for f in self.feedback_history 
                        if f["user_id"] == user_id]
        
        if not user_feedback:
            return {"user_id": user_id, "interactions": 0}
        
        total = len(user_feedback)
        helpful = sum(1 for f in user_feedback if f["helpful"])
        
        category_stats = {}
        for f in user_feedback:
            cat = f["category"]
            if cat not in category_stats:
                category_stats[cat] = {"helpful": 0, "total": 0}
            category_stats[cat]["total"] += 1
            if f["helpful"]:
                category_stats[cat]["helpful"] += 1
        
        return {
            "user_id": user_id,
            "total_interactions": total,
            "helpful": helpful,
            "not_helpful": total - helpful,
            "success_rate": (helpful / total * 100) if total > 0 else 0,
            "by_category": category_stats
        }
    
    def get_improvement_recommendations(self) -> List[Dict]:
        """
        Analyze feedback patterns and recommend improvements
        """
        recommendations = []
        
        # Find categories with low success rates
        categories = set(f["category"] for f in self.feedback_history)
        
        for category in categories:
            perf = self.get_category_performance(category)
            if perf.get("success_rate", 0) < 50 and perf.get("total_responses", 0) >= 5:
                recommendations.append({
                    "priority": "high",
                    "category": category,
                    "message": f"Low performance in {category} (success rate: {perf['success_rate']:.1f}%)",
                    "action": f"Review and improve {category} responses"
                })
            elif perf.get("success_rate", 0) < 70 and perf.get("total_responses", 0) >= 3:
                recommendations.append({
                    "priority": "medium",
                    "category": category,
                    "message": f"Moderate performance in {category} (success rate: {perf['success_rate']:.1f}%)",
                    "action": f"Consider optimizing {category} responses"
                })
        
        return recommendations
    
    def should_use_fallback(self, response_id: str) -> bool:
        """
        Determine if a response pattern should fallback to safer option
        """
        score = self.get_response_score(response_id)
        # Use fallback if score is below -0.3 (more negative feedback)
        return score < -0.3
    
    def get_stats(self) -> Dict:
        """Get overall RL statistics"""
        if not self.feedback_history:
            return {"total_feedback": 0, "status": "no_data"}
        
        total = len(self.feedback_history)
        helpful = sum(1 for f in self.feedback_history if f["helpful"])
        
        return {
            "total_feedback": total,
            "helpful": helpful,
            "not_helpful": total - helpful,
            "overall_success_rate": (helpful / total * 100) if total > 0 else 0,
            "last_updated": self.feedback_history[-1]["timestamp"]
        }


def get_rl_service() -> RLFeedbackService:
    """Factory function to create RL service"""
    return RLFeedbackService()
