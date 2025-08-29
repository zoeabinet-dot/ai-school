"""
Emotional Intelligence and Emotion Recognition System
Addis Ababa AI School Management System

This module provides advanced emotional intelligence capabilities including:
- Facial expression recognition and analysis
- Voice emotion detection and sentiment analysis
- Behavioral pattern recognition
- Multi-modal emotion fusion
- Emotional state tracking and prediction
- Intervention recommendations based on emotional state
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import cv2
import librosa
import face_recognition
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import logging
import json
import os
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmotionRecognitionConfig:
    """Configuration for emotion recognition system."""
    # Model parameters
    facial_model_type: str = 'cnn'  # 'cnn', 'transformer', 'hybrid'
    voice_model_type: str = 'lstm'  # 'lstm', 'transformer', 'cnn'
    behavioral_model_type: str = 'lstm'  # 'lstm', 'transformer', 'gru'
    
    # Emotion categories
    emotion_categories: List[str] = None
    emotion_intensities: List[str] = None
    
    # Feature extraction parameters
    facial_feature_dim: int = 512
    voice_feature_dim: int = 256
    behavioral_feature_dim: int = 128
    
    # Fusion parameters
    fusion_method: str = 'attention'  # 'attention', 'concatenation', 'weighted_average'
    attention_heads: int = 8
    
    # Processing parameters
    frame_rate: int = 30
    audio_sample_rate: int = 16000
    sequence_length: int = 50
    
    def __post_init__(self):
        if self.emotion_categories is None:
            self.emotion_categories = ['happy', 'sad', 'angry', 'fearful', 'surprised', 'disgusted', 'neutral']
        if self.emotion_intensities is None:
            self.emotion_intensities = ['low', 'medium', 'high', 'extreme']

class FacialEmotionRecognizer:
    """Recognizes emotions from facial expressions using computer vision and deep learning."""
    
    def __init__(self, config: EmotionRecognitionConfig):
        self.config = config
        self.model = None
        self.feature_extractor = None
        self.emotion_classifier = None
        self.is_trained = False
        
    def extract_facial_features(self, image: np.ndarray) -> np.ndarray:
        """Extract facial features from an image."""
        try:
            # Detect face landmarks
            face_landmarks = face_recognition.face_landmarks(image)
            
            if not face_landmarks:
                return np.zeros(self.config.facial_feature_dim)
            
            # Extract key facial features
            features = []
            
            for face in face_landmarks:
                # Eye features
                left_eye = face['left_eye']
                right_eye = face['right_eye']
                
                # Calculate eye aspect ratio (EAR)
                left_ear = self._calculate_eye_aspect_ratio(left_eye)
                right_ear = self._calculate_eye_aspect_ratio(right_eye)
                
                # Mouth features
                top_lip = face['top_lip']
                bottom_lip = face['bottom_lip']
                
                # Calculate mouth aspect ratio (MAR)
                mar = self._calculate_mouth_aspect_ratio(top_lip, bottom_lip)
                
                # Eyebrow features
                left_eyebrow = face['left_eyebrow']
                right_eyebrow = face['right_eyebrow']
                
                # Calculate eyebrow positions
                left_eyebrow_height = self._calculate_eyebrow_height(left_eyebrow)
                right_eyebrow_height = self._calculate_eyebrow_height(right_eyebrow)
                
                # Nose features
                nose_bridge = face['nose_bridge']
                nose_tip = face['nose_tip']
                
                # Calculate nose features
                nose_width = self._calculate_nose_width(nose_tip)
                
                # Combine features
                face_features = [
                    left_ear, right_ear, mar,
                    left_eyebrow_height, right_eyebrow_height,
                    nose_width
                ]
                
                # Add geometric features
                geometric_features = self._extract_geometric_features(face)
                face_features.extend(geometric_features)
                
                features.append(face_features)
            
            # Average features if multiple faces detected
            if features:
                avg_features = np.mean(features, axis=0)
                # Pad or truncate to required dimension
                if len(avg_features) < self.config.facial_feature_dim:
                    avg_features = np.pad(avg_features, (0, self.config.facial_feature_dim - len(avg_features)))
                else:
                    avg_features = avg_features[:self.config.facial_feature_dim]
                return avg_features
            else:
                return np.zeros(self.config.facial_feature_dim)
                
        except Exception as e:
            logger.error(f"Error extracting facial features: {e}")
            return np.zeros(self.config.facial_feature_dim)
    
    def _calculate_eye_aspect_ratio(self, eye_points: List[Tuple[int, int]]) -> float:
        """Calculate the eye aspect ratio (EAR) for eye openness detection."""
        if len(eye_points) < 6:
            return 0.0
        
        # Calculate vertical distances
        v1 = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
        v2 = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
        
        # Calculate horizontal distance
        h = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
        
        # Calculate EAR
        ear = (v1 + v2) / (2.0 * h) if h > 0 else 0.0
        return ear
    
    def _calculate_mouth_aspect_ratio(self, top_lip: List[Tuple[int, int]], 
                                    bottom_lip: List[Tuple[int, int]]) -> float:
        """Calculate the mouth aspect ratio (MAR) for mouth openness detection."""
        if len(top_lip) < 6 or len(bottom_lip) < 6:
            return 0.0
        
        # Calculate vertical distances
        v1 = np.linalg.norm(np.array(top_lip[2]) - np.array(bottom_lip[6]))
        v2 = np.linalg.norm(np.array(top_lip[3]) - np.array(bottom_lip[5]))
        v3 = np.linalg.norm(np.array(top_lip[4]) - np.array(bottom_lip[4]))
        
        # Calculate horizontal distance
        h = np.linalg.norm(np.array(top_lip[0]) - np.array(top_lip[6]))
        
        # Calculate MAR
        mar = (v1 + v2 + v3) / (2.0 * h) if h > 0 else 0.0
        return mar
    
    def _calculate_eyebrow_height(self, eyebrow_points: List[Tuple[int, int]]) -> float:
        """Calculate eyebrow height relative to eye position."""
        if len(eyebrow_points) < 4:
            return 0.0
        
        # Calculate average eyebrow height
        eyebrow_y = np.mean([point[1] for point in eyebrow_points])
        return eyebrow_y
    
    def _calculate_nose_width(self, nose_tip: List[Tuple[int, int]]) -> float:
        """Calculate nose width from nose tip points."""
        if len(nose_tip) < 4:
            return 0.0
        
        # Calculate width from leftmost to rightmost points
        x_coords = [point[0] for point in nose_tip]
        width = max(x_coords) - min(x_coords)
        return width
    
    def _extract_geometric_features(self, face: Dict[str, List[Tuple[int, int]]]) -> List[float]:
        """Extract geometric features from facial landmarks."""
        features = []
        
        # Face proportions
        if 'chin' in face and len(face['chin']) > 0:
            chin_points = face['chin']
            face_width = max(point[0] for point in chin_points) - min(point[0] for point in chin_points)
            face_height = max(point[1] for point in chin_points) - min(point[1] for point in chin_points)
            
            if face_height > 0:
                features.append(face_width / face_height)  # Aspect ratio
            else:
                features.append(1.0)
        else:
            features.append(1.0)
        
        # Symmetry features
        if 'left_eye' in face and 'right_eye' in face:
            left_eye_center = np.mean(face['left_eye'], axis=0)
            right_eye_center = np.mean(face['right_eye'], axis=0)
            
            # Eye distance
            eye_distance = np.linalg.norm(left_eye_center - right_eye_center)
            features.append(eye_distance)
        else:
            features.append(0.0)
        
        # Additional geometric features
        features.extend([0.0] * 8)  # Placeholder for additional features
        
        return features
    
    def recognize_emotion(self, image: np.ndarray) -> Dict[str, Any]:
        """Recognize emotion from facial expression."""
        if not self.is_trained:
            raise ValueError("Model must be trained before emotion recognition")
        
        # Extract features
        features = self.extract_facial_features(image)
        
        # Make prediction
        if self.emotion_classifier:
            # Convert to tensor
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            
            with torch.no_grad():
                emotion_logits = self.emotion_classifier(features_tensor)
                emotion_probs = F.softmax(emotion_logits, dim=1)
                
                # Get predicted emotion and confidence
                predicted_emotion_idx = torch.argmax(emotion_probs, dim=1).item()
                confidence = emotion_probs[0][predicted_emotion_idx].item()
                
                predicted_emotion = self.config.emotion_categories[predicted_emotion_idx]
                
                # Calculate emotion intensity
                intensity = self._calculate_emotion_intensity(emotion_probs[0])
                
                return {
                    'emotion': predicted_emotion,
                    'confidence': confidence,
                    'intensity': intensity,
                    'probabilities': emotion_probs[0].numpy().tolist(),
                    'features': features.tolist()
                }
        else:
            # Fallback to basic analysis
            return self._basic_emotion_analysis(features)
    
    def _calculate_emotion_intensity(self, emotion_probs: torch.Tensor) -> str:
        """Calculate emotion intensity based on probability distribution."""
        max_prob = torch.max(emotion_probs).item()
        
        if max_prob > 0.8:
            return 'extreme'
        elif max_prob > 0.6:
            return 'high'
        elif max_prob > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _basic_emotion_analysis(self, features: np.ndarray) -> Dict[str, Any]:
        """Basic emotion analysis when model is not trained."""
        # Simple rule-based analysis based on facial features
        if len(features) >= 6:
            eye_ear = features[0]  # Left eye EAR
            mouth_mar = features[2]  # Mouth MAR
            
            # Simple rules for basic emotion detection
            if eye_ear < 0.2 and mouth_mar > 0.3:
                emotion = 'surprised'
            elif eye_ear < 0.15:
                emotion = 'sad'
            elif mouth_mar > 0.4:
                emotion = 'happy'
            else:
                emotion = 'neutral'
            
            return {
                'emotion': emotion,
                'confidence': 0.5,  # Low confidence for basic analysis
                'intensity': 'medium',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }
        else:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'intensity': 'low',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }

class VoiceEmotionRecognizer:
    """Recognizes emotions from voice using audio processing and deep learning."""
    
    def __init__(self, config: EmotionRecognitionConfig):
        self.config = config
        self.model = None
        self.feature_extractor = None
        self.emotion_classifier = None
        self.is_trained = False
        
    def extract_voice_features(self, audio: np.ndarray) -> np.ndarray:
        """Extract voice features from audio signal."""
        try:
            features = []
            
            # MFCC features
            mfccs = librosa.feature.mfcc(y=audio, sr=self.config.audio_sample_rate, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            mfcc_std = np.std(mfccs, axis=1)
            features.extend(mfcc_mean)
            features.extend(mfcc_std)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.config.audio_sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.config.audio_sample_rate)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=self.config.audio_sample_rate)[0]
            
            features.extend([
                np.mean(spectral_centroids), np.std(spectral_centroids),
                np.mean(spectral_rolloff), np.std(spectral_rolloff),
                np.mean(spectral_bandwidth), np.std(spectral_bandwidth)
            ])
            
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=audio, sr=self.config.audio_sample_rate)
            pitch_mean = np.mean(pitches[magnitudes > 0.1])
            pitch_std = np.std(pitches[magnitudes > 0.1])
            features.extend([pitch_mean, pitch_std])
            
            # Energy features
            rms = librosa.feature.rms(y=audio)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)[0]
            
            features.extend([
                np.mean(rms), np.std(rms),
                np.mean(zero_crossing_rate), np.std(zero_crossing_rate)
            ])
            
            # Tempo features
            tempo, _ = librosa.beat.beat_track(y=audio, sr=self.config.audio_sample_rate)
            features.append(tempo)
            
            # Convert to numpy array and pad/truncate
            features = np.array(features)
            if len(features) < self.config.voice_feature_dim:
                features = np.pad(features, (0, self.config.voice_feature_dim - len(features)))
            else:
                features = features[:self.config.voice_feature_dim]
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting voice features: {e}")
            return np.zeros(self.config.voice_feature_dim)
    
    def recognize_emotion(self, audio: np.ndarray) -> Dict[str, Any]:
        """Recognize emotion from voice."""
        if not self.is_trained:
            raise ValueError("Model must be trained before emotion recognition")
        
        # Extract features
        features = self.extract_voice_features(audio)
        
        # Make prediction
        if self.emotion_classifier:
            # Convert to tensor
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            
            with torch.no_grad():
                emotion_logits = self.emotion_classifier(features_tensor)
                emotion_probs = F.softmax(emotion_logits, dim=1)
                
                # Get predicted emotion and confidence
                predicted_emotion_idx = torch.argmax(emotion_probs, dim=1).item()
                confidence = emotion_probs[0][predicted_emotion_idx].item()
                
                predicted_emotion = self.config.emotion_categories[predicted_emotion_idx]
                
                # Calculate emotion intensity
                intensity = self._calculate_emotion_intensity(emotion_probs[0])
                
                return {
                    'emotion': predicted_emotion,
                    'confidence': confidence,
                    'intensity': intensity,
                    'probabilities': emotion_probs[0].numpy().tolist(),
                    'features': features.tolist()
                }
        else:
            # Fallback to basic analysis
            return self._basic_emotion_analysis(features)
    
    def _calculate_emotion_intensity(self, emotion_probs: torch.Tensor) -> str:
        """Calculate emotion intensity based on probability distribution."""
        max_prob = torch.max(emotion_probs).item()
        
        if max_prob > 0.8:
            return 'extreme'
        elif max_prob > 0.6:
            return 'high'
        elif max_prob > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _basic_emotion_analysis(self, features: np.ndarray) -> Dict[str, Any]:
        """Basic emotion analysis when model is not trained."""
        # Simple rule-based analysis based on voice features
        if len(features) >= 20:
            pitch_mean = features[18]  # Pitch mean
            energy_mean = features[20]  # Energy mean
            tempo = features[24]  # Tempo
            
            # Simple rules for basic emotion detection
            if pitch_mean > 200 and energy_mean > 0.1:
                emotion = 'happy'
            elif pitch_mean < 150 and energy_mean < 0.05:
                emotion = 'sad'
            elif energy_mean > 0.15:
                emotion = 'angry'
            else:
                emotion = 'neutral'
            
            return {
                'emotion': emotion,
                'confidence': 0.5,  # Low confidence for basic analysis
                'intensity': 'medium',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }
        else:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'intensity': 'low',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }

class BehavioralEmotionRecognizer:
    """Recognizes emotions from behavioral patterns and interactions."""
    
    def __init__(self, config: EmotionRecognitionConfig):
        self.config = config
        self.model = None
        self.feature_extractor = None
        self.emotion_classifier = None
        self.is_trained = False
        
    def extract_behavioral_features(self, behavior_data: pd.DataFrame) -> np.ndarray:
        """Extract behavioral features from interaction data."""
        try:
            features = []
            
            # Typing patterns
            if 'typing_speed' in behavior_data.columns:
                typing_speed = behavior_data['typing_speed'].mean()
                typing_variability = behavior_data['typing_speed'].std()
                features.extend([typing_speed, typing_variability])
            else:
                features.extend([0.0, 0.0])
            
            # Mouse movement patterns
            if 'mouse_speed' in behavior_data.columns:
                mouse_speed = behavior_data['mouse_speed'].mean()
                mouse_variability = behavior_data['mouse_speed'].std()
                features.extend([mouse_speed, mouse_variability])
            else:
                features.extend([0.0, 0.0])
            
            # Click patterns
            if 'click_frequency' in behavior_data.columns:
                click_freq = behavior_data['click_frequency'].mean()
                click_pattern = behavior_data['click_frequency'].std()
                features.extend([click_freq, click_pattern])
            else:
                features.extend([0.0, 0.0])
            
            # Response time patterns
            if 'response_time' in behavior_data.columns:
                response_time = behavior_data['response_time'].mean()
                response_variability = behavior_data['response_time'].std()
                features.extend([response_time, response_variability])
            else:
                features.extend([0.0, 0.0])
            
            # Session duration patterns
            if 'session_duration' in behavior_data.columns:
                session_duration = behavior_data['session_duration'].mean()
                features.append(session_duration)
            else:
                features.append(0.0)
            
            # Error patterns
            if 'error_count' in behavior_data.columns:
                error_count = behavior_data['error_count'].sum()
                error_rate = error_count / len(behavior_data) if len(behavior_data) > 0 else 0.0
                features.extend([error_count, error_rate])
            else:
                features.extend([0.0, 0.0])
            
            # Engagement patterns
            if 'engagement_score' in behavior_data.columns:
                engagement = behavior_data['engagement_score'].mean()
                engagement_variability = behavior_data['engagement_score'].std()
                features.extend([engagement, engagement_variability])
            else:
                features.extend([0.0, 0.0])
            
            # Convert to numpy array and pad/truncate
            features = np.array(features)
            if len(features) < self.config.behavioral_feature_dim:
                features = np.pad(features, (0, self.config.behavioral_feature_dim - len(features)))
            else:
                features = features[:self.config.behavioral_feature_dim]
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting behavioral features: {e}")
            return np.zeros(self.config.behavioral_feature_dim)
    
    def recognize_emotion(self, behavior_data: pd.DataFrame) -> Dict[str, Any]:
        """Recognize emotion from behavioral patterns."""
        if not self.is_trained:
            raise ValueError("Model must be trained before emotion recognition")
        
        # Extract features
        features = self.extract_behavioral_features(behavior_data)
        
        # Make prediction
        if self.emotion_classifier:
            # Convert to tensor
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            
            with torch.no_grad():
                emotion_logits = self.emotion_classifier(features_tensor)
                emotion_probs = F.softmax(emotion_logits, dim=1)
                
                # Get predicted emotion and confidence
                predicted_emotion_idx = torch.argmax(emotion_logits, dim=1).item()
                confidence = emotion_probs[0][predicted_emotion_idx].item()
                
                predicted_emotion = self.config.emotion_categories[predicted_emotion_idx]
                
                # Calculate emotion intensity
                intensity = self._calculate_emotion_intensity(emotion_probs[0])
                
                return {
                    'emotion': predicted_emotion,
                    'confidence': confidence,
                    'intensity': intensity,
                    'probabilities': emotion_probs[0].numpy().tolist(),
                    'features': features.tolist()
                }
        else:
            # Fallback to basic analysis
            return self._basic_emotion_analysis(features)
    
    def _calculate_emotion_intensity(self, emotion_probs: torch.Tensor) -> str:
        """Calculate emotion intensity based on probability distribution."""
        max_prob = torch.max(emotion_probs).item()
        
        if max_prob > 0.8:
            return 'extreme'
        elif max_prob > 0.6:
            return 'high'
        elif max_prob > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _basic_emotion_analysis(self, features: np.ndarray) -> Dict[str, Any]:
        """Basic emotion analysis when model is not trained."""
        # Simple rule-based analysis based on behavioral features
        if len(features) >= 15:
            typing_speed = features[0]
            mouse_speed = features[2]
            error_rate = features[9]
            engagement = features[11]
            
            # Simple rules for basic emotion detection
            if error_rate > 0.3 and engagement < 0.4:
                emotion = 'frustrated'
            elif typing_speed > 0.8 and engagement > 0.7:
                emotion = 'happy'
            elif mouse_speed < 0.3 and engagement < 0.5:
                emotion = 'sad'
            else:
                emotion = 'neutral'
            
            return {
                'emotion': emotion,
                'confidence': 0.5,  # Low confidence for basic analysis
                'intensity': 'medium',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }
        else:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'intensity': 'low',
                'probabilities': [0.1] * len(self.config.emotion_categories),
                'features': features.tolist()
            }

class MultiModalEmotionFusion:
    """Fuses emotions from multiple modalities for improved recognition accuracy."""
    
    def __init__(self, config: EmotionRecognitionConfig):
        self.config = config
        self.fusion_model = None
        self.is_trained = False
        
    def fuse_emotions(self, facial_emotion: Dict[str, Any], 
                     voice_emotion: Dict[str, Any],
                     behavioral_emotion: Dict[str, Any]) -> Dict[str, Any]:
        """Fuse emotions from multiple modalities."""
        logger.info("Fusing emotions from multiple modalities...")
        
        if self.is_trained and self.fusion_model:
            return self._learned_fusion(facial_emotion, voice_emotion, behavioral_emotion)
        else:
            return self._rule_based_fusion(facial_emotion, voice_emotion, behavioral_emotion)
    
    def _learned_fusion(self, facial_emotion: Dict[str, Any], 
                        voice_emotion: Dict[str, Any],
                        behavioral_emotion: Dict[str, Any]) -> Dict[str, Any]:
        """Use learned fusion model to combine emotions."""
        # Prepare input features
        facial_features = np.array(facial_emotion['features'])
        voice_features = np.array(voice_emotion['features'])
        behavioral_features = np.array(behavioral_emotion['features'])
        
        # Combine features
        combined_features = np.concatenate([
            facial_features, voice_features, behavioral_features
        ])
        
        # Convert to tensor
        features_tensor = torch.FloatTensor(combined_features).unsqueeze(0)
        
        with torch.no_grad():
            # Get fusion output
            fusion_output = self.fusion_model(features_tensor)
            
            # Extract emotion probabilities and confidence
            emotion_probs = F.softmax(fusion_output['emotion_logits'], dim=1)
            confidence = fusion_output['confidence'].item()
            
            # Get predicted emotion
            predicted_emotion_idx = torch.argmax(emotion_probs, dim=1).item()
            predicted_emotion = self.config.emotion_categories[predicted_emotion_idx]
            
            # Calculate intensity
            intensity = self._calculate_fused_intensity(emotion_probs[0])
            
            return {
                'emotion': predicted_emotion,
                'confidence': confidence,
                'intensity': intensity,
                'probabilities': emotion_probs[0].numpy().tolist(),
                'modality_contributions': {
                    'facial': facial_emotion['confidence'],
                    'voice': voice_emotion['confidence'],
                    'behavioral': behavioral_emotion['confidence']
                },
                'fusion_method': 'learned'
            }
    
    def _rule_based_fusion(self, facial_emotion: Dict[str, Any], 
                           voice_emotion: Dict[str, Any],
                           behavioral_emotion: Dict[str, Any]) -> Dict[str, Any]:
        """Use rule-based fusion to combine emotions."""
        # Weight each modality based on confidence
        facial_weight = facial_emotion['confidence']
        voice_weight = voice_emotion['confidence']
        behavioral_weight = behavioral_emotion['confidence']
        
        # Normalize weights
        total_weight = facial_weight + voice_weight + behavioral_weight
        if total_weight > 0:
            facial_weight /= total_weight
            voice_weight /= total_weight
            behavioral_weight /= total_weight
        else:
            facial_weight = voice_weight = behavioral_weight = 1.0 / 3.0
        
        # Weighted average of emotion probabilities
        fused_probabilities = np.zeros(len(self.config.emotion_categories))
        
        for i in range(len(self.config.emotion_categories)):
            fused_probabilities[i] = (
                facial_emotion['probabilities'][i] * facial_weight +
                voice_emotion['probabilities'][i] * voice_weight +
                behavioral_emotion['probabilities'][i] * behavioral_weight
            )
        
        # Get predicted emotion
        predicted_emotion_idx = np.argmax(fused_probabilities)
        predicted_emotion = self.config.emotion_categories[predicted_emotion_idx]
        
        # Calculate confidence as weighted average
        confidence = (
            facial_emotion['confidence'] * facial_weight +
            voice_emotion['confidence'] * voice_weight +
            behavioral_emotion['confidence'] * behavioral_weight
        )
        
        # Calculate intensity
        intensity = self._calculate_fused_intensity(fused_probabilities)
        
        return {
            'emotion': predicted_emotion,
            'confidence': confidence,
            'intensity': intensity,
            'probabilities': fused_probabilities.tolist(),
            'modality_contributions': {
                'facial': facial_weight,
                'voice': voice_weight,
                'behavioral': behavioral_weight
            },
            'fusion_method': 'rule_based'
        }
    
    def _calculate_fused_intensity(self, probabilities: np.ndarray) -> str:
        """Calculate emotion intensity from fused probabilities."""
        max_prob = np.max(probabilities)
        
        if max_prob > 0.8:
            return 'extreme'
        elif max_prob > 0.6:
            return 'high'
        elif max_prob > 0.4:
            return 'medium'
        else:
            return 'low'

class EmotionalIntelligenceEngine:
    """Main engine that orchestrates all emotional intelligence components."""
    
    def __init__(self, config: EmotionRecognitionConfig):
        self.config = config
        self.facial_recognizer = FacialEmotionRecognizer(config)
        self.voice_recognizer = VoiceEmotionRecognizer(config)
        self.behavioral_recognizer = BehavioralEmotionRecognizer(config)
        self.emotion_fusion = MultiModalEmotionFusion(config)
        self.emotion_history = []
        
    def analyze_emotional_state(self, facial_image: np.ndarray = None,
                               voice_audio: np.ndarray = None,
                               behavior_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Analyze emotional state using available modalities."""
        logger.info("Analyzing emotional state...")
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'modalities_used': [],
            'facial_analysis': None,
            'voice_analysis': None,
            'behavioral_analysis': None,
            'fused_emotion': None,
            'emotional_insights': {},
            'recommendations': []
        }
        
        # Analyze facial expressions
        if facial_image is not None:
            try:
                facial_emotion = self.facial_recognizer.recognize_emotion(facial_image)
                analysis_results['facial_analysis'] = facial_emotion
                analysis_results['modalities_used'].append('facial')
                logger.info(f"Facial emotion detected: {facial_emotion['emotion']}")
            except Exception as e:
                logger.error(f"Error in facial emotion recognition: {e}")
        
        # Analyze voice
        if voice_audio is not None:
            try:
                voice_emotion = self.voice_recognizer.recognize_emotion(voice_audio)
                analysis_results['voice_analysis'] = voice_emotion
                analysis_results['modalities_used'].append('voice')
                logger.info(f"Voice emotion detected: {voice_emotion['emotion']}")
            except Exception as e:
                logger.error(f"Error in voice emotion recognition: {e}")
        
        # Analyze behavior
        if behavior_data is not None:
            try:
                behavioral_emotion = self.behavioral_recognizer.recognize_emotion(behavior_data)
                analysis_results['behavioral_analysis'] = behavioral_emotion
                analysis_results['modalities_used'].append('behavioral')
                logger.info(f"Behavioral emotion detected: {behavioral_emotion['emotion']}")
            except Exception as e:
                logger.error(f"Error in behavioral emotion recognition: {e}")
        
        # Fuse emotions if multiple modalities are available
        if len(analysis_results['modalities_used']) > 1:
            try:
                fused_emotion = self.emotion_fusion.fuse_emotions(
                    analysis_results['facial_analysis'] or {},
                    analysis_results['voice_analysis'] or {},
                    analysis_results['behavioral_analysis'] or {}
                )
                analysis_results['fused_emotion'] = fused_emotion
                logger.info(f"Fused emotion: {fused_emotion['emotion']}")
            except Exception as e:
                logger.error(f"Error in emotion fusion: {e}")
        
        # Generate emotional insights
        analysis_results['emotional_insights'] = self._generate_emotional_insights(analysis_results)
        
        # Generate recommendations
        analysis_results['recommendations'] = self._generate_emotion_recommendations(analysis_results)
        
        # Store in history
        self.emotion_history.append(analysis_results)
        
        logger.info("Emotional state analysis complete")
        return analysis_results
    
    def _generate_emotional_insights(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from emotional analysis."""
        insights = {
            'emotional_stability': 'unknown',
            'dominant_emotion': 'unknown',
            'emotion_transitions': 'unknown',
            'stress_level': 'unknown',
            'engagement_level': 'unknown'
        }
        
        # Determine dominant emotion
        if analysis_results['fused_emotion']:
            insights['dominant_emotion'] = analysis_results['fused_emotion']['emotion']
        elif analysis_results['facial_analysis']:
            insights['dominant_emotion'] = analysis_results['facial_analysis']['emotion']
        elif analysis_results['voice_analysis']:
            insights['dominant_emotion'] = analysis_results['voice_analysis']['emotion']
        elif analysis_results['behavioral_analysis']:
            insights['dominant_emotion'] = analysis_results['behavioral_analysis']['emotion']
        
        # Analyze emotional stability
        if len(self.emotion_history) > 1:
            recent_emotions = [h.get('fused_emotion', {}).get('emotion', 'unknown') 
                              for h in self.emotion_history[-5:]]
            unique_emotions = len(set(recent_emotions))
            
            if unique_emotions <= 2:
                insights['emotional_stability'] = 'high'
            elif unique_emotions <= 4:
                insights['emotional_stability'] = 'medium'
            else:
                insights['emotional_stability'] = 'low'
        
        # Determine stress level
        if insights['dominant_emotion'] in ['angry', 'fearful', 'sad']:
            insights['stress_level'] = 'high'
        elif insights['dominant_emotion'] in ['surprised', 'disgusted']:
            insights['stress_level'] = 'medium'
        else:
            insights['stress_level'] = 'low'
        
        # Determine engagement level
        if analysis_results['behavioral_analysis']:
            engagement = analysis_results['behavioral_analysis'].get('features', [0.0])[11]  # engagement score
            if engagement > 0.7:
                insights['engagement_level'] = 'high'
            elif engagement > 0.4:
                insights['engagement_level'] = 'medium'
            else:
                insights['engagement_level'] = 'low'
        
        return insights
    
    def _generate_emotion_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on emotional state."""
        recommendations = []
        
        dominant_emotion = analysis_results.get('emotional_insights', {}).get('dominant_emotion', 'unknown')
        stress_level = analysis_results.get('emotional_insights', {}).get('stress_level', 'unknown')
        engagement_level = analysis_results.get('emotional_insights', {}).get('engagement_level', 'unknown')
        
        # Emotion-specific recommendations
        if dominant_emotion == 'sad':
            recommendations.extend([
                'Consider taking a short break to refresh',
                'Try engaging in a different type of activity',
                'Consider reaching out to a teacher or counselor'
            ])
        elif dominant_emotion == 'angry':
            recommendations.extend([
                'Take deep breaths and count to ten',
                'Step away from the current task briefly',
                'Consider discussing the issue with a teacher'
            ])
        elif dominant_emotion == 'fearful':
            recommendations.extend([
                'Break down the task into smaller, manageable parts',
                'Ask for clarification or help when needed',
                'Remember that making mistakes is part of learning'
            ])
        
        # Stress-level recommendations
        if stress_level == 'high':
            recommendations.extend([
                'Practice stress-reduction techniques like deep breathing',
                'Consider taking a longer break to relax',
                'Talk to a teacher or counselor about stress management'
            ])
        
        # Engagement-level recommendations
        if engagement_level == 'low':
            recommendations.extend([
                'Try a different learning approach or format',
                'Set small, achievable goals for the session',
                'Take short breaks to maintain focus'
            ])
        
        # General recommendations
        recommendations.extend([
            'Stay hydrated and take regular breaks',
            'Maintain good posture and ergonomics',
            'Communicate with teachers about any concerns'
        ])
        
        return recommendations
    
    def get_emotion_trends(self, time_window: timedelta = timedelta(days=7)) -> Dict[str, Any]:
        """Get emotion trends over a specified time window."""
        cutoff_time = datetime.now() - time_window
        
        # Filter recent history
        recent_history = [
            entry for entry in self.emotion_history
            if datetime.fromisoformat(entry['timestamp']) > cutoff_time
        ]
        
        if not recent_history:
            return {'message': 'No emotion data available for the specified time window'}
        
        # Analyze trends
        emotions = [entry.get('fused_emotion', {}).get('emotion', 'unknown') 
                   for entry in recent_history]
        
        # Count emotions
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate trends
        trends = {
            'total_analyses': len(recent_history),
            'emotion_distribution': emotion_counts,
            'most_common_emotion': max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'unknown',
            'emotional_stability': self._calculate_emotional_stability(emotions),
            'stress_trend': self._calculate_stress_trend(recent_history)
        }
        
        return trends
    
    def _calculate_emotional_stability(self, emotions: List[str]) -> str:
        """Calculate emotional stability based on emotion variety."""
        unique_emotions = len(set(emotions))
        total_emotions = len(emotions)
        
        if total_emotions == 0:
            return 'unknown'
        
        stability_ratio = unique_emotions / total_emotions
        
        if stability_ratio <= 0.3:
            return 'high'
        elif stability_ratio <= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_stress_trend(self, history: List[Dict[str, Any]]) -> str:
        """Calculate stress trend over time."""
        stress_emotions = ['angry', 'fearful', 'sad']
        
        stress_counts = []
        for entry in history:
            emotion = entry.get('fused_emotion', {}).get('emotion', 'unknown')
            stress_counts.append(1 if emotion in stress_emotions else 0)
        
        if len(stress_counts) < 2:
            return 'insufficient_data'
        
        # Calculate trend
        recent_stress = np.mean(stress_counts[-3:]) if len(stress_counts) >= 3 else stress_counts[-1]
        earlier_stress = np.mean(stress_counts[:-3]) if len(stress_counts) >= 3 else stress_counts[0]
        
        if recent_stress > earlier_stress + 0.2:
            return 'increasing'
        elif recent_stress < earlier_stress - 0.2:
            return 'decreasing'
        else:
            return 'stable'

# Example usage
if __name__ == "__main__":
    # Example configuration
    config = EmotionRecognitionConfig(
        facial_model_type='cnn',
        voice_model_type='lstm',
        behavioral_model_type='lstm',
        fusion_method='attention',
        facial_feature_dim=512,
        voice_feature_dim=256,
        behavioral_feature_dim=128
    )
    
    # Create emotional intelligence engine
    emotion_engine = EmotionalIntelligenceEngine(config)
    
    # Example analysis (with placeholder data)
    logger.info("Emotional intelligence system created successfully!")
    
    # Note: In a real implementation, you would:
    # 1. Train the models with actual data
    # 2. Process real facial images, voice recordings, and behavioral data
    # 3. Integrate with the monitoring system for real-time analysis
    # 4. Store results in the database for tracking and analysis