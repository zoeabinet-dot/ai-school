"""
AI/ML Package for Addis Ababa AI School Management System

This package provides advanced artificial intelligence and machine learning capabilities
for educational purposes, including:

- Predictive Analytics and Performance Prediction
- Adaptive Learning and Personalized Content
- Emotional Intelligence and Emotion Recognition
- Custom Neural Network Models
- Advanced Training Pipelines
- Multi-modal Data Processing
"""

__version__ = "1.0.0"
__author__ = "Addis Ababa AI School Development Team"

# Import main components
from .ai_ml_service import AIServiceManager, AIServiceAPI, AIServiceConfig
from .neural_networks import ModelFactory, EducationalTransformer
from .pipelines.training_pipeline import AdvancedTrainer, ModelEvaluator
from .analytics.predictive_analytics import StudentPerformancePredictor, RiskAssessmentEngine
from .adaptive_learning.adaptive_learning_engine import AdaptiveLearningEngine
from .emotional_intelligence.emotion_recognition import EmotionalIntelligenceEngine

__all__ = [
    'AIServiceManager',
    'AIServiceAPI', 
    'AIServiceConfig',
    'ModelFactory',
    'EducationalTransformer',
    'AdvancedTrainer',
    'ModelEvaluator',
    'StudentPerformancePredictor',
    'RiskAssessmentEngine',
    'AdaptiveLearningEngine',
    'EmotionalIntelligenceEngine'
]