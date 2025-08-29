"""
Predictive Analytics System for Educational AI
Addis Ababa AI School Management System

This module provides advanced predictive analytics capabilities including:
- Student performance prediction
- Risk assessment and early warning systems
- Intervention recommendation engines
- Learning outcome forecasting
- Academic trajectory analysis
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, mean_squared_error, r2_score
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
class PredictionConfig:
    """Configuration for predictive analytics models."""
    # Model parameters
    model_type: str  # 'neural_network', 'random_forest', 'gradient_boosting', 'logistic_regression'
    prediction_horizon: int = 1  # Number of time periods to predict ahead
    confidence_threshold: float = 0.8
    risk_threshold: float = 0.7
    
    # Feature engineering
    use_temporal_features: bool = True
    use_interaction_features: bool = True
    use_derived_features: bool = True
    
    # Training parameters
    validation_split: float = 0.2
    test_split: float = 0.1
    cross_validation_folds: int = 5
    
    # Risk assessment
    risk_categories: List[str] = None
    intervention_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.risk_categories is None:
            self.risk_categories = ['low', 'medium', 'high', 'critical']
        if self.intervention_thresholds is None:
            self.intervention_thresholds = {
                'low': 0.3,
                'medium': 0.5,
                'high': 0.7,
                'critical': 0.9
            }

class EducationalPredictor:
    """Base class for educational prediction models."""
    
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for prediction."""
        raise NotImplementedError("Subclasses must implement prepare_features")
    
    def train(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Train the prediction model."""
        raise NotImplementedError("Subclasses must implement train")
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        raise NotImplementedError("Subclasses must implement predict")
    
    def evaluate(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance."""
        raise NotImplementedError("Subclasses must implement evaluate")
    
    def save_model(self, filepath: str):
        """Save the trained model."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_data = {
            'config': asdict(self.config),
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        # Save model-specific data
        if hasattr(self, 'model'):
            model_data['model'] = self.model
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained model."""
        model_data = joblib.load(filepath)
        
        self.config = PredictionConfig(**model_data['config'])
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        if 'model' in model_data:
            self.model = model_data['model']
        
        logger.info(f"Model loaded from {filepath}")

class StudentPerformancePredictor(EducationalPredictor):
    """Predictor for student academic performance."""
    
    def __init__(self, config: PredictionConfig):
        super().__init__(config)
        self.label_encoder = LabelEncoder()
        
    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for performance prediction."""
        logger.info("Preparing features for performance prediction...")
        
        # Select relevant features
        feature_columns = [
            'study_time', 'attendance_rate', 'previous_grades', 'homework_completion',
            'participation_rate', 'test_scores', 'assignment_scores', 'class_engagement',
            'peer_interaction', 'teacher_feedback', 'family_support', 'learning_environment',
            'health_status', 'sleep_hours', 'nutrition_quality', 'stress_level',
            'motivation_level', 'learning_style', 'cognitive_ability', 'emotional_state'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_columns if col in data.columns]
        self.feature_names = available_features
        
        # Handle missing values
        for col in available_features:
            if data[col].dtype in ['int64', 'float64']:
                data[col] = data[col].fillna(data[col].median())
            else:
                data[col] = data[col].fillna(data[col].mode()[0])
        
        # Create derived features
        if self.config.use_derived_features:
            data = self._create_derived_features(data, available_features)
        
        # Create interaction features
        if self.config.use_interaction_features:
            data = self._create_interaction_features(data, available_features)
        
        # Create temporal features
        if self.config.use_temporal_features and 'timestamp' in data.columns:
            data = self._create_temporal_features(data)
        
        # Prepare final feature matrix
        features = data[available_features].values
        
        # Scale features
        features = self.scaler.fit_transform(features)
        
        logger.info(f"Feature preparation complete. Shape: {features.shape}")
        return features
    
    def _create_derived_features(self, data: pd.DataFrame, base_features: List[str]) -> pd.DataFrame:
        """Create derived features for performance prediction."""
        # Academic performance indicators
        if 'previous_grades' in base_features:
            data['grade_trend'] = data['previous_grades'].diff()
            data['grade_volatility'] = data['previous_grades'].rolling(window=3).std()
        
        if 'test_scores' in base_features and 'assignment_scores' in base_features:
            data['score_consistency'] = abs(data['test_scores'] - data['assignment_scores'])
        
        # Study behavior indicators
        if 'study_time' in base_features:
            data['study_efficiency'] = data['previous_grades'] / (data['study_time'] + 1)
            data['study_consistency'] = data['study_time'].rolling(window=7).std()
        
        # Engagement indicators
        if 'participation_rate' in base_features and 'class_engagement' in base_features:
            data['overall_engagement'] = (data['participation_rate'] + data['class_engagement']) / 2
        
        # Health and wellness indicators
        if 'sleep_hours' in base_features and 'stress_level' in base_features:
            data['wellness_score'] = (data['sleep_hours'] / 8) * (1 - data['stress_level'])
        
        return data
    
    def _create_interaction_features(self, data: pd.DataFrame, base_features: List[str]) -> pd.DataFrame:
        """Create interaction features between important variables."""
        # Study time interactions
        if 'study_time' in base_features and 'attendance_rate' in base_features:
            data['study_attendance_interaction'] = data['study_time'] * data['attendance_rate']
        
        if 'study_time' in base_features and 'previous_grades' in base_features:
            data['study_grade_interaction'] = data['study_time'] * data['previous_grades']
        
        # Engagement interactions
        if 'participation_rate' in base_features and 'peer_interaction' in base_features:
            data['social_engagement'] = data['participation_rate'] * data['peer_interaction']
        
        # Support interactions
        if 'family_support' in base_features and 'teacher_feedback' in base_features:
            data['support_network'] = data['family_support'] * data['teacher_feedback']
        
        return data
    
    def _create_temporal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create temporal features from timestamp data."""
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Time-based features
        data['hour_of_day'] = data['timestamp'].dt.hour
        data['day_of_week'] = data['timestamp'].dt.dayofweek
        data['month'] = data['timestamp'].dt.month
        data['quarter'] = data['timestamp'].dt.quarter
        data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
        data['is_morning'] = data['hour_of_day'].between(6, 12).astype(int)
        data['is_afternoon'] = data['hour_of_day'].between(12, 18).astype(int)
        data['is_evening'] = data['hour_of_day'].between(18, 22).astype(int)
        
        return data
    
    def train(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Train the performance prediction model."""
        logger.info("Training performance prediction model...")
        
        # Encode targets if they're categorical
        if targets.dtype == 'object':
            targets = self.label_encoder.fit_transform(targets)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            features, targets, test_size=self.config.validation_split, random_state=42, stratify=targets
        )
        
        # Create and train model
        if self.config.model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif self.config.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif self.config.model_type == 'logistic_regression':
            self.model = LogisticRegression(random_state=42, max_iter=1000)
        elif self.config.model_type == 'neural_network':
            # This would use the custom neural network models
            raise NotImplementedError("Neural network training not implemented in this class")
        else:
            raise ValueError(f"Unknown model type: {self.config.model_type}")
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate on validation set
        val_predictions = self.model.predict(X_val)
        val_accuracy = accuracy_score(y_val, val_predictions)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, features, targets, cv=self.config.cross_validation_folds)
        
        self.is_trained = True
        
        metrics = {
            'validation_accuracy': val_accuracy,
            'cross_validation_mean': cv_scores.mean(),
            'cross_validation_std': cv_scores.std(),
            'training_samples': len(X_train),
            'validation_samples': len(X_val)
        }
        
        logger.info(f"Training complete. Validation accuracy: {val_accuracy:.4f}")
        return metrics
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict student performance."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        predictions = self.model.predict(features_scaled)
        
        # Decode predictions if using label encoder
        if hasattr(self, 'label_encoder') and hasattr(self.label_encoder, 'inverse_transform'):
            predictions = self.label_encoder.inverse_transform(predictions)
        
        return predictions
    
    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        """Predict performance probabilities."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get probabilities
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features_scaled)
        else:
            # For models without predict_proba, create dummy probabilities
            predictions = self.model.predict(features_scaled)
            probabilities = np.zeros((len(predictions), len(np.unique(predictions))))
            for i, pred in enumerate(predictions):
                probabilities[i, pred] = 1.0
        
        return probabilities
    
    def evaluate(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance."""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Encode targets if needed
        if targets.dtype == 'object' and hasattr(self, 'label_encoder'):
            targets = self.label_encoder.transform(targets)
        
        # Make predictions
        predictions = self.predict(features)
        
        # Calculate metrics
        accuracy = accuracy_score(targets, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(targets, predictions, average='weighted')
        
        # Calculate educational-specific metrics
        educational_metrics = self._calculate_educational_metrics(targets, predictions)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            **educational_metrics
        }
        
        return metrics
    
    def _calculate_educational_metrics(self, targets: np.ndarray, predictions: np.ndarray) -> Dict[str, float]:
        """Calculate metrics specific to educational performance prediction."""
        # Grade prediction accuracy (assuming grades are ordered)
        grade_accuracy = self._calculate_grade_accuracy(targets, predictions)
        
        # Risk assessment accuracy
        risk_accuracy = self._calculate_risk_accuracy(targets, predictions)
        
        # Improvement prediction accuracy
        improvement_accuracy = self._calculate_improvement_accuracy(targets, predictions)
        
        return {
            'grade_accuracy': grade_accuracy,
            'risk_accuracy': risk_accuracy,
            'improvement_accuracy': improvement_accuracy
        }
    
    def _calculate_grade_accuracy(self, targets: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy considering grade proximity."""
        # Define grade proximity weights
        grade_weights = np.array([
            [1.0, 0.8, 0.6, 0.4, 0.2],  # A
            [0.8, 1.0, 0.8, 0.6, 0.4],  # B
            [0.6, 0.8, 1.0, 0.8, 0.6],  # C
            [0.4, 0.6, 0.8, 1.0, 0.8],  # D
            [0.2, 0.4, 0.6, 0.8, 1.0]   # F
        ])
        
        weighted_accuracy = 0.0
        for target, pred in zip(targets, predictions):
            if target < len(grade_weights) and pred < len(grade_weights[0]):
                weighted_accuracy += grade_weights[target][pred]
        
        return weighted_accuracy / len(targets) if len(targets) > 0 else 0.0
    
    def _calculate_risk_accuracy(self, targets: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy for identifying at-risk students."""
        # Define at-risk grades (D and F)
        at_risk_grades = [3, 4]  # Assuming 0=A, 1=B, 2=C, 3=D, 4=F
        
        at_risk_targets = np.isin(targets, at_risk_grades)
        at_risk_predictions = np.isin(predictions, at_risk_grades)
        
        return accuracy_score(at_risk_targets, at_risk_predictions)
    
    def _calculate_improvement_accuracy(self, targets: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy for predicting improvement trends."""
        # This would require historical data to calculate trends
        # For now, return a placeholder
        return 0.0

class RiskAssessmentEngine:
    """Engine for assessing student risk levels and generating early warnings."""
    
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.risk_models = {}
        self.risk_thresholds = config.intervention_thresholds
        
    def assess_student_risk(self, student_data: pd.DataFrame, 
                           performance_predictor: StudentPerformancePredictor) -> Dict[str, Any]:
        """Assess comprehensive risk for a student."""
        logger.info("Assessing student risk levels...")
        
        risk_assessment = {
            'academic_risk': self._assess_academic_risk(student_data, performance_predictor),
            'behavioral_risk': self._assess_behavioral_risk(student_data),
            'emotional_risk': self._assess_emotional_risk(student_data),
            'social_risk': self._assess_social_risk(student_data),
            'health_risk': self._assess_health_risk(student_data),
            'overall_risk': None,
            'risk_category': None,
            'intervention_recommendations': []
        }
        
        # Calculate overall risk
        risk_assessment['overall_risk'] = self._calculate_overall_risk(risk_assessment)
        risk_assessment['risk_category'] = self._categorize_risk(risk_assessment['overall_risk'])
        
        # Generate intervention recommendations
        risk_assessment['intervention_recommendations'] = self._generate_interventions(risk_assessment)
        
        return risk_assessment
    
    def _assess_academic_risk(self, student_data: pd.DataFrame, 
                             performance_predictor: StudentPerformancePredictor) -> Dict[str, Any]:
        """Assess academic risk factors."""
        academic_indicators = {
            'grade_decline': 0.0,
            'attendance_issues': 0.0,
            'homework_completion': 0.0,
            'test_performance': 0.0,
            'study_habits': 0.0,
            'overall_score': 0.0
        }
        
        # Grade decline analysis
        if 'previous_grades' in student_data.columns:
            grades = student_data['previous_grades'].dropna()
            if len(grades) > 1:
                grade_trend = np.polyfit(range(len(grades)), grades, 1)[0]
                academic_indicators['grade_decline'] = max(0, -grade_trend) / 10
        
        # Attendance issues
        if 'attendance_rate' in student_data.columns:
            attendance = student_data['attendance_rate'].mean()
            academic_indicators['attendance_issues'] = max(0, 0.8 - attendance)
        
        # Homework completion
        if 'homework_completion' in student_data.columns:
            hw_completion = student_data['homework_completion'].mean()
            academic_indicators['homework_completion'] = max(0, 0.8 - hw_completion)
        
        # Test performance
        if 'test_scores' in student_data.columns:
            test_scores = student_data['test_scores'].mean()
            academic_indicators['test_performance'] = max(0, 0.7 - test_scores)
        
        # Study habits
        if 'study_time' in student_data.columns:
            study_time = student_data['study_time'].mean()
            academic_indicators['study_habits'] = max(0, 2 - study_time) / 5
        
        # Calculate overall academic risk score
        academic_indicators['overall_score'] = np.mean([
            academic_indicators['grade_decline'],
            academic_indicators['attendance_issues'],
            academic_indicators['homework_completion'],
            academic_indicators['test_performance'],
            academic_indicators['study_habits']
        ])
        
        return academic_indicators
    
    def _assess_behavioral_risk(self, student_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess behavioral risk factors."""
        behavioral_indicators = {
            'classroom_disruption': 0.0,
            'peer_conflicts': 0.0,
            'rule_violations': 0.0,
            'attention_issues': 0.0,
            'overall_score': 0.0
        }
        
        # This would typically use data from monitoring systems
        # For now, use placeholder calculations
        
        behavioral_indicators['overall_score'] = np.mean([
            behavioral_indicators['classroom_disruption'],
            behavioral_indicators['peer_conflicts'],
            behavioral_indicators['rule_violations'],
            behavioral_indicators['attention_issues']
        ])
        
        return behavioral_indicators
    
    def _assess_emotional_risk(self, student_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess emotional risk factors."""
        emotional_indicators = {
            'stress_level': 0.0,
            'anxiety_signs': 0.0,
            'mood_instability': 0.0,
            'self_esteem': 0.0,
            'overall_score': 0.0
        }
        
        # Stress level assessment
        if 'stress_level' in student_data.columns:
            emotional_indicators['stress_level'] = student_data['stress_level'].mean()
        
        # Self-esteem assessment (inverse relationship)
        if 'participation_rate' in student_data.columns:
            participation = student_data['participation_rate'].mean()
            emotional_indicators['self_esteem'] = max(0, 0.5 - participation)
        
        # Calculate overall emotional risk
        emotional_indicators['overall_score'] = np.mean([
            emotional_indicators['stress_level'],
            emotional_indicators['anxiety_signs'],
            emotional_indicators['mood_instability'],
            emotional_indicators['self_esteem']
        ])
        
        return emotional_indicators
    
    def _assess_social_risk(self, student_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess social risk factors."""
        social_indicators = {
            'peer_isolation': 0.0,
            'communication_issues': 0.0,
            'group_participation': 0.0,
            'overall_score': 0.0
        }
        
        # Peer interaction assessment
        if 'peer_interaction' in student_data.columns:
            peer_interaction = student_data['peer_interaction'].mean()
            social_indicators['peer_isolation'] = max(0, 0.6 - peer_interaction)
        
        # Group participation
        if 'participation_rate' in student_data.columns:
            participation = student_data['participation_rate'].mean()
            social_indicators['group_participation'] = max(0, 0.7 - participation)
        
        # Calculate overall social risk
        social_indicators['overall_score'] = np.mean([
            social_indicators['peer_isolation'],
            social_indicators['communication_issues'],
            social_indicators['group_participation']
        ])
        
        return social_indicators
    
    def _assess_health_risk(self, student_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess health and wellness risk factors."""
        health_indicators = {
            'sleep_quality': 0.0,
            'nutrition_issues': 0.0,
            'physical_activity': 0.0,
            'overall_score': 0.0
        }
        
        # Sleep quality assessment
        if 'sleep_hours' in student_data.columns:
            sleep_hours = student_data['sleep_hours'].mean()
            if sleep_hours < 7:
                health_indicators['sleep_quality'] = (7 - sleep_hours) / 7
            elif sleep_hours > 9:
                health_indicators['sleep_quality'] = (sleep_hours - 9) / 3
        
        # Calculate overall health risk
        health_indicators['overall_score'] = np.mean([
            health_indicators['sleep_quality'],
            health_indicators['nutrition_issues'],
            health_indicators['physical_activity']
        ])
        
        return health_indicators
    
    def _calculate_overall_risk(self, risk_assessment: Dict[str, Any]) -> float:
        """Calculate overall risk score from individual risk assessments."""
        risk_scores = [
            risk_assessment['academic_risk']['overall_score'],
            risk_assessment['behavioral_risk']['overall_score'],
            risk_assessment['emotional_risk']['overall_score'],
            risk_assessment['social_risk']['overall_score'],
            risk_assessment['health_risk']['overall_score']
        ]
        
        # Weight different risk factors
        weights = [0.4, 0.2, 0.2, 0.1, 0.1]  # Academic risk gets highest weight
        
        overall_risk = np.average(risk_scores, weights=weights)
        return min(1.0, overall_risk)  # Cap at 1.0
    
    def _categorize_risk(self, overall_risk: float) -> str:
        """Categorize risk level based on overall risk score."""
        if overall_risk < 0.3:
            return 'low'
        elif overall_risk < 0.5:
            return 'medium'
        elif overall_risk < 0.7:
            return 'high'
        else:
            return 'critical'
    
    def _generate_interventions(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate intervention recommendations based on risk assessment."""
        interventions = []
        
        risk_category = risk_assessment['risk_category']
        overall_risk = risk_assessment['overall_risk']
        
        # Academic interventions
        if risk_assessment['academic_risk']['overall_score'] > 0.5:
            interventions.append({
                'type': 'academic',
                'priority': 'high' if overall_risk > 0.7 else 'medium',
                'description': 'Implement academic support program',
                'actions': [
                    'Schedule tutoring sessions',
                    'Provide additional homework support',
                    'Implement study skills training',
                    'Regular progress monitoring'
                ]
            })
        
        # Behavioral interventions
        if risk_assessment['behavioral_risk']['overall_score'] > 0.5:
            interventions.append({
                'type': 'behavioral',
                'priority': 'high' if overall_risk > 0.7 else 'medium',
                'description': 'Address behavioral concerns',
                'actions': [
                    'Behavior modification plan',
                    'Positive reinforcement strategies',
                    'Conflict resolution training',
                    'Parent-teacher communication'
                ]
            })
        
        # Emotional interventions
        if risk_assessment['emotional_risk']['overall_score'] > 0.5:
            interventions.append({
                'type': 'emotional',
                'priority': 'high' if overall_risk > 0.7 else 'medium',
                'description': 'Provide emotional support',
                'actions': [
                    'Counseling services',
                    'Stress management techniques',
                    'Emotional regulation training',
                    'Support group participation'
                ]
            })
        
        # Social interventions
        if risk_assessment['social_risk']['overall_score'] > 0.5:
            interventions.append({
                'type': 'social',
                'priority': 'medium',
                'description': 'Improve social skills',
                'actions': [
                    'Social skills training',
                    'Peer mentoring program',
                    'Group activities',
                    'Communication workshops'
                ]
            })
        
        # Health interventions
        if risk_assessment['health_risk']['overall_score'] > 0.5:
            interventions.append({
                'type': 'health',
                'priority': 'medium',
                'description': 'Address health concerns',
                'actions': [
                    'Sleep hygiene education',
                    'Nutrition guidance',
                    'Physical activity promotion',
                    'Health monitoring'
                ]
            })
        
        # Critical risk interventions
        if risk_category == 'critical':
            interventions.append({
                'type': 'emergency',
                'priority': 'critical',
                'description': 'Immediate intervention required',
                'actions': [
                    'Immediate parent contact',
                    'School counselor involvement',
                    'External professional referral',
                    'Safety assessment'
                ]
            })
        
        return interventions

class InterventionRecommendationEngine:
    """Engine for generating personalized intervention recommendations."""
    
    def __init__(self):
        self.intervention_templates = self._load_intervention_templates()
        self.effectiveness_data = self._load_effectiveness_data()
    
    def generate_recommendations(self, student_profile: Dict[str, Any], 
                               risk_assessment: Dict[str, Any],
                               performance_history: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate personalized intervention recommendations."""
        logger.info("Generating personalized intervention recommendations...")
        
        recommendations = []
        
        # Academic interventions
        academic_recs = self._generate_academic_interventions(student_profile, risk_assessment, performance_history)
        recommendations.extend(academic_recs)
        
        # Behavioral interventions
        behavioral_recs = self._generate_behavioral_interventions(student_profile, risk_assessment)
        recommendations.extend(behavioral_recs)
        
        # Emotional interventions
        emotional_recs = self._generate_emotional_interventions(student_profile, risk_assessment)
        recommendations.extend(emotional_recs)
        
        # Social interventions
        social_recs = self._generate_social_interventions(student_profile, risk_assessment)
        recommendations.extend(social_recs)
        
        # Health interventions
        health_recs = self._generate_health_interventions(student_profile, risk_assessment)
        recommendations.extend(health_recs)
        
        # Sort recommendations by priority and expected effectiveness
        recommendations = self._prioritize_recommendations(recommendations, student_profile)
        
        return recommendations
    
    def _load_intervention_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load intervention templates from configuration."""
        return {
            'academic': [
                {
                    'name': 'Tutoring Program',
                    'description': 'One-on-one or small group tutoring',
                    'duration': '8-12 weeks',
                    'frequency': '2-3 times per week',
                    'expected_improvement': 0.15,
                    'cost': 'medium',
                    'resources_required': ['tutor', 'materials', 'space']
                },
                {
                    'name': 'Study Skills Workshop',
                    'description': 'Comprehensive study skills training',
                    'duration': '4-6 weeks',
                    'frequency': 'Once per week',
                    'expected_improvement': 0.10,
                    'cost': 'low',
                    'resources_required': ['instructor', 'materials']
                },
                {
                    'name': 'Homework Support',
                    'description': 'Structured homework assistance program',
                    'duration': 'Ongoing',
                    'frequency': 'Daily',
                    'expected_improvement': 0.08,
                    'cost': 'low',
                    'resources_required': ['supervisor', 'space']
                }
            ],
            'behavioral': [
                {
                    'name': 'Behavior Modification Plan',
                    'description': 'Structured behavior improvement program',
                    'duration': '6-12 weeks',
                    'frequency': 'Daily monitoring',
                    'expected_improvement': 0.20,
                    'cost': 'medium',
                    'resources_required': ['behavioral specialist', 'monitoring tools']
                }
            ],
            'emotional': [
                {
                    'name': 'Counseling Services',
                    'description': 'Professional emotional support',
                    'duration': 'Ongoing',
                    'frequency': 'Weekly',
                    'expected_improvement': 0.25,
                    'cost': 'high',
                    'resources_required': ['counselor', 'private space']
                }
            ]
        }
    
    def _load_effectiveness_data(self) -> Dict[str, Dict[str, float]]:
        """Load intervention effectiveness data."""
        return {
            'tutoring': {
                'math': 0.18,
                'science': 0.15,
                'language': 0.12,
                'overall': 0.15
            },
            'study_skills': {
                'all_subjects': 0.10,
                'overall': 0.10
            },
            'counseling': {
                'emotional': 0.25,
                'behavioral': 0.20,
                'overall': 0.22
            }
        }
    
    def _generate_academic_interventions(self, student_profile: Dict[str, Any],
                                       risk_assessment: Dict[str, Any],
                                       performance_history: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate academic intervention recommendations."""
        recommendations = []
        
        academic_risk = risk_assessment['academic_risk']['overall_score']
        
        if academic_risk > 0.5:
            # Analyze subject-specific performance
            subject_performance = self._analyze_subject_performance(performance_history)
            
            for subject, performance in subject_performance.items():
                if performance < 0.7:  # Below 70%
                    recommendations.append({
                        'type': 'academic',
                        'subject': subject,
                        'intervention': 'Tutoring Program',
                        'priority': 'high' if academic_risk > 0.7 else 'medium',
                        'description': f'Subject-specific tutoring for {subject}',
                        'expected_improvement': self.effectiveness_data['tutoring'].get(subject, 0.15),
                        'duration': '8-12 weeks',
                        'frequency': '2-3 times per week',
                        'resources': ['subject tutor', 'materials', 'practice space']
                    })
            
            # General academic support
            if academic_risk > 0.6:
                recommendations.append({
                    'type': 'academic',
                    'subject': 'general',
                    'intervention': 'Study Skills Workshop',
                    'priority': 'medium',
                    'description': 'Comprehensive study skills improvement',
                    'expected_improvement': 0.10,
                    'duration': '4-6 weeks',
                    'frequency': 'Once per week',
                    'resources': ['study skills instructor', 'materials']
                })
        
        return recommendations
    
    def _analyze_subject_performance(self, performance_history: pd.DataFrame) -> Dict[str, float]:
        """Analyze performance by subject."""
        subject_performance = {}
        
        # This would analyze actual subject-specific data
        # For now, return placeholder data
        subjects = ['math', 'science', 'language', 'social_studies']
        for subject in subjects:
            if f'{subject}_score' in performance_history.columns:
                subject_performance[subject] = performance_history[f'{subject}_score'].mean()
            else:
                subject_performance[subject] = 0.75  # Placeholder
        
        return subject_performance
    
    def _generate_behavioral_interventions(self, student_profile: Dict[str, Any],
                                         risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate behavioral intervention recommendations."""
        recommendations = []
        
        behavioral_risk = risk_assessment['behavioral_risk']['overall_score']
        
        if behavioral_risk > 0.5:
            recommendations.append({
                'type': 'behavioral',
                'intervention': 'Behavior Modification Plan',
                'priority': 'high' if behavioral_risk > 0.7 else 'medium',
                'description': 'Structured behavior improvement program',
                'expected_improvement': 0.20,
                'duration': '6-12 weeks',
                'frequency': 'Daily monitoring',
                'resources': ['behavioral specialist', 'monitoring tools', 'parent involvement']
            })
        
        return recommendations
    
    def _generate_emotional_interventions(self, student_profile: Dict[str, Any],
                                        risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate emotional intervention recommendations."""
        recommendations = []
        
        emotional_risk = risk_assessment['emotional_risk']['overall_score']
        
        if emotional_risk > 0.5:
            recommendations.append({
                'type': 'emotional',
                'intervention': 'Counseling Services',
                'priority': 'high' if emotional_risk > 0.7 else 'medium',
                'description': 'Professional emotional support and guidance',
                'expected_improvement': 0.25,
                'duration': 'Ongoing',
                'frequency': 'Weekly',
                'resources': ['school counselor', 'private space', 'parent communication']
            })
        
        return recommendations
    
    def _generate_social_interventions(self, student_profile: Dict[str, Any],
                                      risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate social intervention recommendations."""
        recommendations = []
        
        social_risk = risk_assessment['social_risk']['overall_score']
        
        if social_risk > 0.5:
            recommendations.append({
                'type': 'social',
                'intervention': 'Social Skills Training',
                'priority': 'medium',
                'description': 'Improve peer interaction and communication skills',
                'expected_improvement': 0.15,
                'duration': '6-8 weeks',
                'frequency': 'Twice per week',
                'resources': ['social skills instructor', 'group activities', 'peer mentors']
            })
        
        return recommendations
    
    def _generate_health_interventions(self, student_profile: Dict[str, Any],
                                      risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate health intervention recommendations."""
        recommendations = []
        
        health_risk = risk_assessment['health_risk']['overall_score']
        
        if health_risk > 0.5:
            recommendations.append({
                'type': 'health',
                'intervention': 'Wellness Program',
                'priority': 'medium',
                'description': 'Improve sleep, nutrition, and physical activity',
                'expected_improvement': 0.12,
                'duration': '8-10 weeks',
                'frequency': 'Weekly sessions',
                'resources': ['health educator', 'nutritionist', 'fitness instructor']
            })
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, Any]],
                                   student_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize recommendations based on multiple factors."""
        for rec in recommendations:
            # Calculate priority score
            priority_score = 0
            
            # Risk level priority
            if rec['priority'] == 'critical':
                priority_score += 100
            elif rec['priority'] == 'high':
                priority_score += 80
            elif rec['priority'] == 'medium':
                priority_score += 60
            else:
                priority_score += 40
            
            # Expected improvement priority
            priority_score += rec.get('expected_improvement', 0) * 100
            
            # Resource availability priority
            if self._check_resource_availability(rec['resources']):
                priority_score += 20
            
            # Student preference priority (if available)
            if 'student_preferences' in student_profile:
                if rec['type'] in student_profile['student_preferences']:
                    priority_score += 15
            
            rec['priority_score'] = priority_score
        
        # Sort by priority score (descending)
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return recommendations
    
    def _check_resource_availability(self, resources: List[str]) -> bool:
        """Check if required resources are available."""
        # This would check actual resource availability
        # For now, return True as placeholder
        return True

# Example usage
if __name__ == "__main__":
    # Example configuration
    config = PredictionConfig(
        model_type='random_forest',
        prediction_horizon=1,
        confidence_threshold=0.8,
        risk_threshold=0.7
    )
    
    # Create predictor
    predictor = StudentPerformancePredictor(config)
    
    # Create risk assessment engine
    risk_engine = RiskAssessmentEngine(config)
    
    # Create intervention engine
    intervention_engine = InterventionRecommendationEngine()
    
    logger.info("Predictive analytics system created successfully!")