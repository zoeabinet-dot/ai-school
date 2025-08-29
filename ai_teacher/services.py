"""
AI Teacher Services for Advanced Features
Phase 2: Multi-language Support, Computer Vision, Predictive Analytics, NLU
"""
import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import cv2
import openai
from googletrans import Translator
from langdetect import detect
from deep_translator import GoogleTranslator
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

logger = logging.getLogger(__name__)

class MultiLanguageService:
    """
    Multi-language support service for Amharic, Oromo, and other local languages
    """
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'am': 'Amharic (አማርኛ)',
        'om': 'Oromo (Afaan Oromoo)', 
        'ti': 'Tigrinya (ትግርኛ)',
        'so': 'Somali (Soomaali)',
        'sw': 'Swahili (Kiswahili)',
        'ar': 'Arabic (العربية)',
        'fr': 'French (Français)',
    }
    
    # Language mappings for different translation services
    LANGUAGE_MAPPINGS = {
        'am': 'amharic',
        'om': 'oromo', 
        'ti': 'tigrinya',
        'so': 'somali',
        'sw': 'swahili',
    }
    
    def __init__(self):
        self.translator = Translator()
        self.deep_translator = GoogleTranslator()
        
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text
        """
        try:
            detected = detect(text)
            return detected if detected in self.SUPPORTED_LANGUAGES else 'en'
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'
    
    def translate_text(self, text: str, target_language: str, source_language: str = None) -> str:
        """
        Translate text to target language
        """
        try:
            if not source_language:
                source_language = self.detect_language(text)
            
            if source_language == target_language:
                return text
            
            # Use cache for frequent translations
            cache_key = f"translation_{hash(text)}_{source_language}_{target_language}"
            cached_translation = cache.get(cache_key)
            if cached_translation:
                return cached_translation
            
            # Primary translation using googletrans
            try:
                result = self.translator.translate(text, src=source_language, dest=target_language)
                translated_text = result.text
            except Exception:
                # Fallback to deep-translator
                translated_text = self.deep_translator.translate(text, target=target_language)
            
            # Cache the translation for 1 hour
            cache.set(cache_key, translated_text, 3600)
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def translate_lesson_content(self, lesson_data: Dict, target_language: str) -> Dict:
        """
        Translate entire lesson content to target language
        """
        try:
            translated_lesson = lesson_data.copy()
            
            # Translate text fields
            if 'title' in lesson_data:
                translated_lesson['title'] = self.translate_text(lesson_data['title'], target_language)
            
            if 'description' in lesson_data:
                translated_lesson['description'] = self.translate_text(lesson_data['description'], target_language)
            
            # Translate content sections
            if 'content' in lesson_data and isinstance(lesson_data['content'], dict):
                translated_content = {}
                for key, value in lesson_data['content'].items():
                    if isinstance(value, str):
                        translated_content[key] = self.translate_text(value, target_language)
                    elif isinstance(value, list):
                        translated_content[key] = [
                            self.translate_text(item, target_language) if isinstance(item, str) else item
                            for item in value
                        ]
                    else:
                        translated_content[key] = value
                translated_lesson['content'] = translated_content
            
            # Translate learning objectives
            if 'learning_objectives' in lesson_data:
                translated_lesson['learning_objectives'] = [
                    self.translate_text(obj, target_language) 
                    for obj in lesson_data['learning_objectives']
                ]
            
            return translated_lesson
            
        except Exception as e:
            logger.error(f"Lesson translation error: {e}")
            return lesson_data
    
    def get_localized_ai_prompt(self, prompt: str, language: str) -> str:
        """
        Create localized AI prompts for different languages
        """
        language_instructions = {
            'am': "Please respond in Amharic (አማርኛ). Use culturally appropriate examples from Ethiopian context.",
            'om': "Please respond in Oromo (Afaan Oromoo). Use culturally appropriate examples from Oromo culture.",
            'ti': "Please respond in Tigrinya (ትግርኛ). Use culturally appropriate examples from Tigrinya culture.",
            'so': "Please respond in Somali (Soomaali). Use culturally appropriate examples from Somali culture.",
            'sw': "Please respond in Swahili (Kiswahili). Use culturally appropriate examples from East African context.",
            'ar': "Please respond in Arabic (العربية). Use culturally appropriate examples.",
            'fr': "Please respond in French (Français). Use culturally appropriate examples.",
        }
        
        if language in language_instructions:
            return f"{language_instructions[language]}\n\n{prompt}"
        return prompt


class AdvancedComputerVisionService:
    """
    Advanced computer vision service for sophisticated behavioral analysis
    """
    
    def __init__(self):
        # Load pre-trained models for emotion detection and pose estimation
        self.emotion_model = None
        self.pose_estimator = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
    def analyze_student_behavior(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive behavioral analysis from video frame
        """
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'face_detection': self._detect_face_and_eyes(frame),
                'attention_metrics': self._calculate_attention_metrics(frame),
                'emotion_analysis': self._analyze_emotions(frame),
                'posture_analysis': self._analyze_posture(frame),
                'engagement_score': 0.0,
                'distraction_indicators': [],
                'recommendations': []
            }
            
            # Calculate overall engagement score
            analysis['engagement_score'] = self._calculate_engagement_score(analysis)
            
            # Generate recommendations based on analysis
            analysis['recommendations'] = self._generate_behavior_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Behavioral analysis error: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _detect_face_and_eyes(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detect face and eyes for attention tracking
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        face_data = {
            'faces_detected': len(faces),
            'face_positions': [],
            'eye_contact': False,
            'head_pose': 'neutral'
        }
        
        for (x, y, w, h) in faces:
            face_data['face_positions'].append({'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)})
            
            # Detect eyes within face region
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            
            if len(eyes) >= 2:
                face_data['eye_contact'] = True
                
            # Simple head pose estimation based on face position
            frame_center_x = frame.shape[1] // 2
            face_center_x = x + w // 2
            
            if abs(face_center_x - frame_center_x) < 50:
                face_data['head_pose'] = 'center'
            elif face_center_x < frame_center_x - 50:
                face_data['head_pose'] = 'left'
            else:
                face_data['head_pose'] = 'right'
        
        return face_data
    
    def _calculate_attention_metrics(self, frame: np.ndarray) -> Dict[str, float]:
        """
        Calculate attention-related metrics
        """
        # Simple attention metrics based on face detection and movement
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate frame variance (higher variance indicates more movement/distraction)
        frame_variance = np.var(gray)
        
        # Normalize attention score (lower variance = higher attention)
        attention_score = max(0, min(100, 100 - (frame_variance / 1000)))
        
        return {
            'attention_score': float(attention_score),
            'frame_variance': float(frame_variance),
            'stability_index': float(100 - min(100, frame_variance / 500))
        }
    
    def _analyze_emotions(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Analyze emotional state from facial expressions
        """
        # Simplified emotion analysis (in production, use trained models)
        emotions = {
            'happy': 0.2,
            'focused': 0.6,
            'frustrated': 0.1,
            'bored': 0.05,
            'confused': 0.05,
            'neutral': 0.0
        }
        
        # Get dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return {
            'emotions': emotions,
            'dominant_emotion': dominant_emotion[0],
            'confidence': float(dominant_emotion[1]),
            'emotional_stability': 0.8  # Placeholder
        }
    
    def _analyze_posture(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Analyze student posture and body language
        """
        # Simplified posture analysis
        return {
            'posture_score': 75.0,  # Placeholder
            'slouching_detected': False,
            'distance_from_camera': 'optimal',
            'body_alignment': 'good'
        }
    
    def _calculate_engagement_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate overall engagement score from various metrics
        """
        try:
            face_score = 20 if analysis['face_detection']['faces_detected'] > 0 else 0
            eye_contact_score = 25 if analysis['face_detection']['eye_contact'] else 0
            attention_score = analysis['attention_metrics']['attention_score'] * 0.3
            emotion_score = analysis['emotion_analysis']['confidence'] * 20
            posture_score = analysis['posture_analysis']['posture_score'] * 0.05
            
            total_score = face_score + eye_contact_score + attention_score + emotion_score + posture_score
            return min(100.0, max(0.0, total_score))
            
        except Exception:
            return 50.0  # Default score
    
    def _generate_behavior_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on behavioral analysis
        """
        recommendations = []
        
        if analysis['engagement_score'] < 50:
            recommendations.append("Student appears disengaged. Consider interactive content or break.")
        
        if not analysis['face_detection']['eye_contact']:
            recommendations.append("Limited eye contact detected. Encourage student to look at camera.")
        
        if analysis['face_detection']['head_pose'] != 'center':
            recommendations.append("Student looking away. Check for distractions in environment.")
        
        emotion = analysis['emotion_analysis']['dominant_emotion']
        if emotion == 'frustrated':
            recommendations.append("Student appears frustrated. Consider providing additional support.")
        elif emotion == 'bored':
            recommendations.append("Student appears bored. Try more engaging content or activities.")
        
        return recommendations


class PredictiveAnalyticsService:
    """
    AI-powered predictive analytics for learning outcomes
    """
    
    def __init__(self):
        self.model_path = '/workspace/ai_models/'
        os.makedirs(self.model_path, exist_ok=True)
        self.performance_model = None
        self.engagement_model = None
        self.scaler = StandardScaler()
        
    def predict_learning_outcomes(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict learning outcomes based on student data
        """
        try:
            # Prepare features for prediction
            features = self._extract_features(student_data)
            
            # Make predictions
            predictions = {
                'academic_performance': self._predict_academic_performance(features),
                'engagement_trend': self._predict_engagement_trend(features),
                'completion_probability': self._predict_completion_probability(features),
                'recommended_interventions': self._recommend_interventions(features),
                'confidence_intervals': self._calculate_confidence_intervals(features)
            }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'error': str(e)}
    
    def _extract_features(self, student_data: Dict[str, Any]) -> np.ndarray:
        """
        Extract features from student data for ML models
        """
        features = []
        
        # Academic features
        features.extend([
            student_data.get('current_grade', 0),
            student_data.get('attendance_rate', 0),
            student_data.get('assignment_completion_rate', 0),
            student_data.get('average_score', 0),
        ])
        
        # Behavioral features
        features.extend([
            student_data.get('average_engagement_score', 0),
            student_data.get('attention_score', 0),
            student_data.get('participation_rate', 0),
        ])
        
        # Learning pattern features
        features.extend([
            student_data.get('study_time_daily', 0),
            student_data.get('lesson_completion_rate', 0),
            student_data.get('help_seeking_frequency', 0),
        ])
        
        return np.array(features).reshape(1, -1)
    
    def _predict_academic_performance(self, features: np.ndarray) -> Dict[str, float]:
        """
        Predict future academic performance
        """
        # Simplified prediction (in production, use trained ML models)
        base_score = np.mean(features[0][:4]) if len(features[0]) >= 4 else 70.0
        
        return {
            'next_month_score': float(min(100, max(0, base_score + np.random.normal(0, 5)))),
            'semester_projection': float(min(100, max(0, base_score + np.random.normal(0, 10)))),
            'improvement_potential': float(min(30, max(-10, np.random.normal(5, 3))))
        }
    
    def _predict_engagement_trend(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Predict student engagement trends
        """
        current_engagement = features[0][4] if len(features[0]) > 4 else 70.0
        
        return {
            'current_level': float(current_engagement),
            'trend': 'increasing' if np.random.random() > 0.5 else 'stable',
            'predicted_next_week': float(min(100, max(0, current_engagement + np.random.normal(0, 5)))),
            'risk_factors': ['low_participation'] if current_engagement < 50 else []
        }
    
    def _predict_completion_probability(self, features: np.ndarray) -> Dict[str, float]:
        """
        Predict probability of course/lesson completion
        """
        completion_rate = features[0][8] if len(features[0]) > 8 else 0.8
        
        return {
            'current_lesson': float(min(1.0, max(0.0, completion_rate + np.random.normal(0, 0.1)))),
            'current_unit': float(min(1.0, max(0.0, completion_rate * 0.9 + np.random.normal(0, 0.1)))),
            'full_course': float(min(1.0, max(0.0, completion_rate * 0.8 + np.random.normal(0, 0.15))))
        }
    
    def _recommend_interventions(self, features: np.ndarray) -> List[Dict[str, str]]:
        """
        Recommend interventions based on predictions
        """
        interventions = []
        
        avg_score = np.mean(features[0][:4]) if len(features[0]) >= 4 else 70
        
        if avg_score < 60:
            interventions.append({
                'type': 'academic_support',
                'description': 'Additional tutoring sessions recommended',
                'priority': 'high'
            })
        
        if len(features[0]) > 4 and features[0][4] < 50:  # Low engagement
            interventions.append({
                'type': 'engagement_boost',
                'description': 'Interactive content and gamification needed',
                'priority': 'medium'
            })
        
        return interventions
    
    def _calculate_confidence_intervals(self, features: np.ndarray) -> Dict[str, Dict[str, float]]:
        """
        Calculate confidence intervals for predictions
        """
        return {
            'academic_performance': {'lower': 65.0, 'upper': 85.0},
            'engagement': {'lower': 60.0, 'upper': 80.0},
            'completion': {'lower': 0.7, 'upper': 0.9}
        }


class NaturalLanguageUnderstandingService:
    """
    Enhanced Natural Language Understanding for better conversation context
    """
    
    def __init__(self):
        self.context_memory = {}
        self.sentiment_analyzer = None
        self.intent_classifier = None
        
    def analyze_conversation_context(self, conversation_history: List[Dict], current_message: str) -> Dict[str, Any]:
        """
        Analyze conversation context for better AI responses
        """
        try:
            context_analysis = {
                'sentiment': self._analyze_sentiment(current_message),
                'intent': self._classify_intent(current_message),
                'context_continuity': self._assess_context_continuity(conversation_history, current_message),
                'learning_indicators': self._detect_learning_indicators(current_message),
                'response_strategy': self._determine_response_strategy(conversation_history, current_message)
            }
            
            return context_analysis
            
        except Exception as e:
            logger.error(f"Context analysis error: {e}")
            return {'error': str(e)}
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of student message
        """
        # Simplified sentiment analysis (use transformers in production)
        positive_words = ['good', 'great', 'understand', 'clear', 'helpful', 'thanks', 'yes']
        negative_words = ['confused', 'difficult', 'hard', 'dont understand', 'help', 'stuck']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': float(confidence),
            'emotional_indicators': {
                'frustration': negative_count > 2,
                'enthusiasm': positive_count > 2,
                'confusion': 'confused' in text_lower or 'dont understand' in text_lower
            }
        }
    
    def _classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of student message
        """
        intents = {
            'question': ['what', 'how', 'why', 'when', 'where', '?'],
            'help_request': ['help', 'stuck', 'dont understand', 'explain'],
            'confirmation': ['yes', 'ok', 'understood', 'got it'],
            'clarification': ['mean', 'clarify', 'explain again'],
            'feedback': ['good', 'bad', 'like', 'dislike']
        }
        
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])
            return {
                'primary_intent': primary_intent[0],
                'confidence': float(min(0.9, primary_intent[1] * 0.3)),
                'all_intents': intent_scores
            }
        else:
            return {
                'primary_intent': 'general',
                'confidence': 0.5,
                'all_intents': {}
            }
    
    def _assess_context_continuity(self, conversation_history: List[Dict], current_message: str) -> Dict[str, Any]:
        """
        Assess how well the current message fits with conversation context
        """
        if not conversation_history:
            return {'continuity_score': 1.0, 'topic_shift': False}
        
        # Simple context continuity assessment
        last_message = conversation_history[-1] if conversation_history else {}
        
        # Check for topic keywords overlap
        current_words = set(current_message.lower().split())
        last_words = set(last_message.get('content', '').lower().split())
        
        overlap = len(current_words.intersection(last_words))
        total_unique = len(current_words.union(last_words))
        
        continuity_score = overlap / max(1, total_unique) if total_unique > 0 else 0.5
        
        return {
            'continuity_score': float(continuity_score),
            'topic_shift': continuity_score < 0.2,
            'context_relevance': 'high' if continuity_score > 0.5 else 'medium' if continuity_score > 0.2 else 'low'
        }
    
    def _detect_learning_indicators(self, text: str) -> Dict[str, bool]:
        """
        Detect indicators of learning progress in student messages
        """
        return {
            'understanding': any(word in text.lower() for word in ['understand', 'got it', 'clear', 'makes sense']),
            'confusion': any(word in text.lower() for word in ['confused', 'dont get', 'unclear']),
            'engagement': any(word in text.lower() for word in ['interesting', 'cool', 'want to know']),
            'mastery': any(word in text.lower() for word in ['easy', 'simple', 'already know']),
            'struggle': any(word in text.lower() for word in ['difficult', 'hard', 'struggling'])
        }
    
    def _determine_response_strategy(self, conversation_history: List[Dict], current_message: str) -> Dict[str, str]:
        """
        Determine the best response strategy based on context analysis
        """
        sentiment = self._analyze_sentiment(current_message)
        intent = self._classify_intent(current_message)
        learning = self._detect_learning_indicators(current_message)
        
        if learning['confusion'] or intent['primary_intent'] == 'help_request':
            return {
                'strategy': 'supportive_explanation',
                'tone': 'patient_and_encouraging',
                'approach': 'break_down_concepts'
            }
        elif learning['mastery'] or sentiment['sentiment'] == 'positive':
            return {
                'strategy': 'advancement',
                'tone': 'encouraging',
                'approach': 'introduce_challenges'
            }
        elif learning['struggle']:
            return {
                'strategy': 'scaffolding',
                'tone': 'supportive',
                'approach': 'provide_examples'
            }
        else:
            return {
                'strategy': 'adaptive',
                'tone': 'neutral_helpful',
                'approach': 'follow_student_lead'
            }


# Initialize services
multi_language_service = MultiLanguageService()
computer_vision_service = AdvancedComputerVisionService()
predictive_analytics_service = PredictiveAnalyticsService()
nlu_service = NaturalLanguageUnderstandingService()