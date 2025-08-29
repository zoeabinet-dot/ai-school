"""
AI/ML Service Integration for Educational AI
Addis Ababa AI School Management System

This module provides a unified interface for all AI/ML capabilities including:
- Predictive analytics and performance prediction
- Adaptive learning and personalized content
- Emotional intelligence and emotion recognition
- Model training and management
- Real-time AI inference services
"""

import numpy as np
import pandas as pd
import torch
import logging
import json
import os
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import AI/ML components
from .neural_networks import ModelFactory, EducationalTransformer, StudentPerformancePredictor as NeuralPredictor
from .pipelines.training_pipeline import TrainingConfig, AdvancedTrainer, ModelEvaluator
from .analytics.predictive_analytics import (
    PredictionConfig, StudentPerformancePredictor, RiskAssessmentEngine, 
    InterventionRecommendationEngine
)
from .adaptive_learning.adaptive_learning_engine import (
    AdaptiveLearningConfig, AdaptiveLearningEngine
)
from .emotional_intelligence.emotion_recognition import (
    EmotionRecognitionConfig, EmotionalIntelligenceEngine
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIServiceConfig:
    """Configuration for the AI/ML service."""
    # Service parameters
    enable_predictive_analytics: bool = True
    enable_adaptive_learning: bool = True
    enable_emotional_intelligence: bool = True
    enable_real_time_inference: bool = True
    
    # Model management
    model_storage_path: str = "models/"
    model_cache_size: int = 10
    auto_model_update: bool = True
    
    # Performance parameters
    batch_size: int = 32
    max_concurrent_requests: int = 100
    request_timeout: int = 30
    
    # Monitoring parameters
    enable_performance_monitoring: bool = True
    log_predictions: bool = True
    log_errors: bool = True

class AIServiceManager:
    """Manages all AI/ML services and provides a unified interface."""
    
    def __init__(self, config: AIServiceConfig):
        self.config = config
        self.services = {}
        self.model_cache = {}
        self.request_queue = []
        self.performance_metrics = {}
        
        # Initialize services
        self._initialize_services()
        
        logger.info("AI/ML Service Manager initialized successfully")
    
    def _initialize_services(self):
        """Initialize all AI/ML services."""
        try:
            # Initialize Predictive Analytics
            if self.config.enable_predictive_analytics:
                pred_config = PredictionConfig(
                    model_type='neural_network',
                    prediction_horizon=1,
                    confidence_threshold=0.8,
                    risk_threshold=0.7
                )
                
                self.services['predictive_analytics'] = {
                    'predictor': StudentPerformancePredictor(pred_config),
                    'risk_engine': RiskAssessmentEngine(pred_config),
                    'intervention_engine': InterventionRecommendationEngine()
                }
                logger.info("Predictive Analytics service initialized")
            
            # Initialize Adaptive Learning
            if self.config.enable_adaptive_learning:
                adaptive_config = AdaptiveLearningConfig(
                    max_path_length=20,
                    difficulty_levels=5,
                    content_variety=10
                )
                
                self.services['adaptive_learning'] = AdaptiveLearningEngine(adaptive_config)
                logger.info("Adaptive Learning service initialized")
            
            # Initialize Emotional Intelligence
            if self.config.enable_emotional_intelligence:
                emotion_config = EmotionRecognitionConfig(
                    facial_model_type='cnn',
                    voice_model_type='lstm',
                    behavioral_model_type='lstm'
                )
                
                self.services['emotional_intelligence'] = EmotionalIntelligenceEngine(emotion_config)
                logger.info("Emotional Intelligence service initialized")
            
            # Initialize Model Factory
            self.services['model_factory'] = ModelFactory()
            logger.info("Model Factory initialized")
            
        except Exception as e:
            logger.error(f"Error initializing AI/ML services: {e}")
            raise
    
    def predict_student_performance(self, student_data: pd.DataFrame, 
                                  student_id: str = None) -> Dict[str, Any]:
        """Predict student academic performance."""
        try:
            if 'predictive_analytics' not in self.services:
                raise ValueError("Predictive Analytics service not available")
            
            predictor = self.services['predictive_analytics']['predictor']
            
            # Prepare features
            features = predictor.prepare_features(student_data)
            
            # Make prediction
            if predictor.is_trained:
                predictions = predictor.predict(features)
                probabilities = predictor.predict_proba(features)
                
                result = {
                    'student_id': student_id,
                    'predictions': predictions.tolist() if hasattr(predictions, 'tolist') else predictions,
                    'probabilities': probabilities.tolist() if hasattr(probabilities, 'tolist') else probabilities,
                    'confidence': np.max(probabilities) if hasattr(probabilities, 'max') else 0.5,
                    'timestamp': datetime.now().isoformat(),
                    'model_status': 'trained'
                }
            else:
                # Use basic prediction if model not trained
                result = {
                    'student_id': student_id,
                    'predictions': ['average'] * len(features),
                    'probabilities': [[0.25, 0.25, 0.25, 0.25]] * len(features),
                    'confidence': 0.25,
                    'timestamp': datetime.now().isoformat(),
                    'model_status': 'untrained',
                    'message': 'Model not trained, using basic predictions'
                }
            
            # Log prediction if enabled
            if self.config.log_predictions:
                self._log_prediction('performance_prediction', result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in performance prediction: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('performance_prediction', error_msg)
            
            return {
                'student_id': student_id,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def assess_student_risk(self, student_data: pd.DataFrame, 
                           student_id: str = None) -> Dict[str, Any]:
        """Assess student risk levels and generate early warnings."""
        try:
            if 'predictive_analytics' not in self.services:
                raise ValueError("Predictive Analytics service not available")
            
            risk_engine = self.services['predictive_analytics']['risk_engine']
            predictor = self.services['predictive_analytics']['predictor']
            
            # Assess risk
            risk_assessment = risk_engine.assess_student_risk(student_data, predictor)
            
            result = {
                'student_id': student_id,
                'risk_assessment': risk_assessment,
                'timestamp': datetime.now().isoformat(),
                'overall_risk': risk_assessment['overall_risk'],
                'risk_category': risk_assessment['risk_category'],
                'interventions': risk_assessment['intervention_recommendations']
            }
            
            # Log assessment if enabled
            if self.config.log_predictions:
                self._log_prediction('risk_assessment', result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error in risk assessment: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('risk_assessment', error_msg)
            
            return {
                'student_id': student_id,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_interventions(self, student_profile: Dict[str, Any],
                             risk_assessment: Dict[str, Any],
                             performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Generate personalized intervention recommendations."""
        try:
            if 'predictive_analytics' not in self.services:
                raise ValueError("Predictive Analytics service not available")
            
            intervention_engine = self.services['predictive_analytics']['intervention_engine']
            
            # Generate recommendations
            recommendations = intervention_engine.generate_recommendations(
                student_profile, risk_assessment, performance_history
            )
            
            result = {
                'student_id': student_profile.get('student_id'),
                'recommendations': recommendations,
                'total_recommendations': len(recommendations),
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error in intervention generation: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('intervention_generation', error_msg)
            
            return {
                'student_id': student_profile.get('student_id'),
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def create_adaptive_learning_experience(self, student_id: str, subject: str,
                                          learning_objectives: List[str],
                                          student_profile: Dict[str, Any],
                                          performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Create a personalized adaptive learning experience."""
        try:
            if 'adaptive_learning' not in self.services:
                raise ValueError("Adaptive Learning service not available")
            
            adaptive_engine = self.services['adaptive_learning']
            
            # Create learning experience
            learning_experience = adaptive_engine.create_personalized_learning_experience(
                student_id, subject, learning_objectives, student_profile, performance_history
            )
            
            result = {
                'student_id': student_id,
                'learning_experience': learning_experience,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error in adaptive learning experience creation: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('adaptive_learning', error_msg)
            
            return {
                'student_id': student_id,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def analyze_emotional_state(self, student_id: str,
                               facial_image: np.ndarray = None,
                               voice_audio: np.ndarray = None,
                               behavior_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Analyze student emotional state using available modalities."""
        try:
            if 'emotional_intelligence' not in self.services:
                raise ValueError("Emotional Intelligence service not available")
            
            emotion_engine = self.services['emotional_intelligence']
            
            # Analyze emotional state
            analysis_results = emotion_engine.analyze_emotional_state(
                facial_image, voice_audio, behavior_data
            )
            
            result = {
                'student_id': student_id,
                'emotional_analysis': analysis_results,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error in emotional state analysis: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('emotional_analysis', error_msg)
            
            return {
                'student_id': student_id,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def train_custom_model(self, model_type: str, training_data: pd.DataFrame,
                          model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Train a custom AI model for educational purposes."""
        try:
            # Create training configuration
            training_config = TrainingConfig(
                model_type=model_type,
                input_size=model_config.get('input_size', 100),
                hidden_sizes=model_config.get('hidden_sizes', [256, 128, 64]),
                output_size=model_config.get('output_size', 10),
                dropout_rate=model_config.get('dropout_rate', 0.3)
            )
            
            # Create trainer
            trainer = AdvancedTrainer(training_config, ModelFactory())
            
            # Prepare data
            features = training_data.drop(columns=['target']).values
            targets = training_data['target'].values
            
            # Train model with hyperparameter optimization
            training_results = trainer.train_with_hyperparameter_optimization(
                (features, targets), n_trials=50
            )
            
            result = {
                'model_type': model_type,
                'training_results': training_results,
                'best_model_path': training_results.get('best_model_path'),
                'timestamp': datetime.now().isoformat(),
                'status': 'completed'
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error in model training: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('model_training', error_msg)
            
            return {
                'model_type': model_type,
                'error': error_msg,
                'timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def get_ai_insights(self, student_id: str, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """Get comprehensive AI insights for a student."""
        try:
            insights = {
                'student_id': student_id,
                'timestamp': datetime.now().isoformat(),
                'performance_insights': {},
                'emotional_insights': {},
                'learning_insights': {},
                'recommendations': []
            }
            
            # Get emotional trends if service available
            if 'emotional_intelligence' in self.services:
                emotion_engine = self.services['emotional_intelligence']
                emotion_trends = emotion_engine.get_emotion_trends(time_window)
                insights['emotional_insights'] = emotion_trends
            
            # Get performance trends (placeholder - would integrate with actual data)
            insights['performance_insights'] = {
                'trend': 'improving',
                'strengths': ['Mathematics', 'Problem Solving'],
                'areas_for_improvement': ['Reading Comprehension'],
                'predicted_performance': 'above_average'
            }
            
            # Get learning insights (placeholder - would integrate with actual data)
            insights['learning_insights'] = {
                'learning_style': 'visual',
                'optimal_study_time': 'morning',
                'preferred_content_format': 'interactive',
                'engagement_level': 'high'
            }
            
            # Generate recommendations
            insights['recommendations'] = [
                'Continue with current study schedule',
                'Focus on reading comprehension exercises',
                'Use visual aids for complex concepts',
                'Take regular breaks to maintain focus'
            ]
            
            return insights
            
        except Exception as e:
            error_msg = f"Error in AI insights generation: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('ai_insights', error_msg)
            
            return {
                'student_id': student_id,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def batch_predict(self, student_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform batch predictions for multiple students."""
        try:
            results = []
            
            for student_data in student_data_list:
                student_id = student_data.get('student_id')
                data_df = pd.DataFrame(student_data.get('data', []))
                
                if not data_df.empty:
                    # Perform performance prediction
                    performance_result = self.predict_student_performance(data_df, student_id)
                    
                    # Perform risk assessment
                    risk_result = self.assess_student_risk(data_df, student_id)
                    
                    # Combine results
                    combined_result = {
                        'student_id': student_id,
                        'performance_prediction': performance_result,
                        'risk_assessment': risk_result,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    results.append(combined_result)
                else:
                    results.append({
                        'student_id': student_id,
                        'error': 'No data provided',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return results
            
        except Exception as e:
            error_msg = f"Error in batch prediction: {e}"
            logger.error(error_msg)
            
            if self.config.log_errors:
                self._log_error('batch_prediction', error_msg)
            
            return [{'error': error_msg, 'timestamp': datetime.now().isoformat()}]
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get the status of all AI/ML services."""
        status = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'overall_status': 'healthy',
            'performance_metrics': self.performance_metrics
        }
        
        # Check each service
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'is_trained'):
                    service_status = 'trained' if service.is_trained else 'untrained'
                elif isinstance(service, dict):
                    # For services with multiple components
                    service_status = 'available'
                else:
                    service_status = 'available'
                
                status['services'][service_name] = {
                    'status': service_status,
                    'available': True
                }
                
            except Exception as e:
                status['services'][service_name] = {
                    'status': 'error',
                    'available': False,
                    'error': str(e)
                }
                status['overall_status'] = 'degraded'
        
        return status
    
    def _log_prediction(self, prediction_type: str, result: Dict[str, Any]):
        """Log prediction results for monitoring."""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'prediction_type': prediction_type,
                'result': result
            }
            
            # Store in performance metrics
            if prediction_type not in self.performance_metrics:
                self.performance_metrics[prediction_type] = []
            
            self.performance_metrics[prediction_type].append(log_entry)
            
            # Keep only recent entries
            if len(self.performance_metrics[prediction_type]) > 100:
                self.performance_metrics[prediction_type] = self.performance_metrics[prediction_type][-50:]
                
        except Exception as e:
            logger.error(f"Error logging prediction: {e}")
    
    def _log_error(self, error_type: str, error_message: str):
        """Log errors for monitoring."""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'error_type': error_type,
                'error_message': error_message
            }
            
            # Store in performance metrics
            if 'errors' not in self.performance_metrics:
                self.performance_metrics['errors'] = []
            
            self.performance_metrics['errors'].append(log_entry)
            
            # Keep only recent errors
            if len(self.performance_metrics['errors']) > 50:
                self.performance_metrics['errors'] = self.performance_metrics['errors'][-25:]
                
        except Exception as e:
            logger.error(f"Error logging error: {e}")

class AIServiceAPI:
    """RESTful API interface for AI/ML services."""
    
    def __init__(self, service_manager: AIServiceManager):
        self.service_manager = service_manager
        logger.info("AI Service API initialized")
    
    def predict_performance(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for performance prediction."""
        try:
            student_id = request_data.get('student_id')
            student_data = pd.DataFrame(request_data.get('student_data', []))
            
            if student_data.empty:
                return {
                    'error': 'No student data provided',
                    'status': 'error'
                }
            
            result = self.service_manager.predict_student_performance(student_data, student_id)
            return {
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def assess_risk(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for risk assessment."""
        try:
            student_id = request_data.get('student_id')
            student_data = pd.DataFrame(request_data.get('student_data', []))
            
            if student_data.empty:
                return {
                    'error': 'No student data provided',
                    'status': 'error'
                }
            
            result = self.service_manager.assess_student_risk(student_data, student_id)
            return {
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def get_adaptive_learning(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for adaptive learning experience."""
        try:
            student_id = request_data.get('student_id')
            subject = request_data.get('subject')
            learning_objectives = request_data.get('learning_objectives', [])
            student_profile = request_data.get('student_profile', {})
            performance_history = pd.DataFrame(request_data.get('performance_history', []))
            
            if not student_id or not subject:
                return {
                    'error': 'Missing required parameters: student_id and subject',
                    'status': 'error'
                }
            
            result = self.service_manager.create_adaptive_learning_experience(
                student_id, subject, learning_objectives, student_profile, performance_history
            )
            
            return {
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def analyze_emotion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for emotional analysis."""
        try:
            student_id = request_data.get('student_id')
            facial_image = request_data.get('facial_image')  # Base64 encoded or file path
            voice_audio = request_data.get('voice_audio')    # Base64 encoded or file path
            behavior_data = pd.DataFrame(request_data.get('behavior_data', []))
            
            if not student_id:
                return {
                    'error': 'Missing required parameter: student_id',
                    'status': 'error'
                }
            
            # Convert base64 data to numpy arrays if needed
            # This is a placeholder - actual implementation would handle file conversion
            
            result = self.service_manager.analyze_emotional_state(
                student_id, facial_image, voice_audio, behavior_data
            )
            
            return {
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def get_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for comprehensive AI insights."""
        try:
            student_id = request_data.get('student_id')
            time_window_days = request_data.get('time_window_days', 30)
            
            if not student_id:
                return {
                    'error': 'Missing required parameter: student_id',
                    'status': 'error'
                }
            
            time_window = timedelta(days=time_window_days)
            result = self.service_manager.get_ai_insights(student_id, time_window)
            
            return {
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """API endpoint for service status."""
        try:
            status = self.service_manager.get_service_status()
            return {
                'data': status,
                'status': 'success'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

# Example usage and testing
if __name__ == "__main__":
    # Example configuration
    config = AIServiceConfig(
        enable_predictive_analytics=True,
        enable_adaptive_learning=True,
        enable_emotional_intelligence=True,
        enable_real_time_inference=True
    )
    
    # Create service manager
    service_manager = AIServiceManager(config)
    
    # Create API interface
    api = AIServiceAPI(service_manager)
    
    # Test service status
    status = api.get_service_status()
    logger.info(f"Service Status: {status['status']}")
    
    # Example student data
    example_student_data = {
        'student_id': 'STU001',
        'student_data': [
            {
                'study_time': 2.5,
                'attendance_rate': 0.9,
                'previous_grades': 0.85,
                'homework_completion': 0.95,
                'participation_rate': 0.8,
                'test_scores': 0.88,
                'assignment_scores': 0.92,
                'class_engagement': 0.85,
                'peer_interaction': 0.75,
                'teacher_feedback': 0.9,
                'family_support': 0.8,
                'learning_environment': 0.85,
                'health_status': 0.9,
                'sleep_hours': 8.0,
                'nutrition_quality': 0.8,
                'stress_level': 0.3,
                'motivation_level': 0.85,
                'learning_style': 'visual',
                'cognitive_ability': 0.9,
                'emotional_state': 'positive'
            }
        ]
    }
    
    # Test performance prediction
    try:
        prediction_result = api.predict_performance(example_student_data)
        logger.info(f"Performance Prediction: {prediction_result['status']}")
        
        if prediction_result['status'] == 'success':
            logger.info(f"Prediction completed for student {prediction_result['data']['student_id']}")
    except Exception as e:
        logger.error(f"Error in performance prediction test: {e}")
    
    # Test risk assessment
    try:
        risk_result = api.assess_risk(example_student_data)
        logger.info(f"Risk Assessment: {risk_result['status']}")
        
        if risk_result['status'] == 'success':
            logger.info(f"Risk assessment completed for student {risk_result['data']['student_id']}")
    except Exception as e:
        logger.error(f"Error in risk assessment test: {e}")
    
    logger.info("AI/ML Service integration testing completed!")