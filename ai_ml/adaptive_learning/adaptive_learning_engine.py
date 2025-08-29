"""
Adaptive Learning Engine for Educational AI
Addis Ababa AI School Management System

This module provides advanced adaptive learning capabilities including:
- Personalized learning path generation
- Dynamic content adaptation
- Learning style optimization
- Difficulty adjustment algorithms
- Progress tracking and optimization
- Multi-modal learning support
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
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
class AdaptiveLearningConfig:
    """Configuration for adaptive learning engine."""
    # Learning path parameters
    max_path_length: int = 20
    min_path_length: int = 5
    branching_factor: int = 3
    
    # Content adaptation parameters
    difficulty_levels: int = 5
    content_variety: int = 10
    adaptation_threshold: float = 0.1
    
    # Learning style parameters
    learning_modalities: List[str] = None
    style_preference_weight: float = 0.3
    performance_weight: float = 0.7
    
    # Optimization parameters
    optimization_iterations: int = 100
    convergence_threshold: float = 0.01
    exploration_rate: float = 0.1
    
    def __post_init__(self):
        if self.learning_modalities is None:
            self.learning_modalities = ['visual', 'auditory', 'kinesthetic', 'reading', 'social']

class LearningPathNode:
    """Represents a node in the learning path."""
    
    def __init__(self, content_id: str, content_type: str, difficulty: float, 
                 prerequisites: List[str] = None, estimated_duration: int = 0):
        self.content_id = content_id
        self.content_type = content_type
        self.difficulty = difficulty
        self.prerequisites = prerequisites or []
        self.estimated_duration = estimated_duration
        self.completion_rate = 0.0
        self.success_rate = 0.0
        self.engagement_score = 0.0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            'content_id': self.content_id,
            'content_type': self.content_type,
            'difficulty': self.difficulty,
            'prerequisites': self.prerequisites,
            'estimated_duration': self.estimated_duration,
            'completion_rate': self.completion_rate,
            'success_rate': self.success_rate,
            'engagement_score': self.engagement_score
        }

class LearningPath:
    """Represents a complete learning path for a student."""
    
    def __init__(self, student_id: str, subject: str, learning_objectives: List[str]):
        self.student_id = student_id
        self.subject = subject
        self.learning_objectives = learning_objectives
        self.nodes: List[LearningPathNode] = []
        self.current_node_index = 0
        self.completion_percentage = 0.0
        self.estimated_completion_time = 0
        self.adaptation_history = []
        
    def add_node(self, node: LearningPathNode):
        """Add a node to the learning path."""
        self.nodes.append(node)
        self._update_estimated_completion_time()
    
    def get_current_node(self) -> Optional[LearningPathNode]:
        """Get the current active node."""
        if 0 <= self.current_node_index < len(self.nodes):
            return self.nodes[self.current_node_index]
        return None
    
    def advance_to_next_node(self):
        """Move to the next node in the path."""
        if self.current_node_index < len(self.nodes) - 1:
            self.current_node_index += 1
            self._update_completion_percentage()
    
    def _update_completion_percentage(self):
        """Update the completion percentage."""
        if self.nodes:
            self.completion_percentage = (self.current_node_index / len(self.nodes)) * 100
    
    def _update_estimated_completion_time(self):
        """Update the estimated completion time."""
        self.estimated_completion_time = sum(node.estimated_duration for node in self.nodes)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert learning path to dictionary."""
        return {
            'student_id': self.student_id,
            'subject': self.subject,
            'learning_objectives': self.learning_objectives,
            'nodes': [node.to_dict() for node in self.nodes],
            'current_node_index': self.current_node_index,
            'completion_percentage': self.completion_percentage,
            'estimated_completion_time': self.estimated_completion_time,
            'adaptation_history': self.adaptation_history
        }

class LearningStyleAnalyzer:
    """Analyzes and determines student learning styles."""
    
    def __init__(self, config: AdaptiveLearningConfig):
        self.config = config
        self.style_classifier = None
        self.style_encoder = LabelEncoder()
        self.is_trained = False
        
    def analyze_learning_style(self, student_data: pd.DataFrame) -> Dict[str, float]:
        """Analyze student's learning style preferences."""
        logger.info("Analyzing student learning style...")
        
        style_scores = {modality: 0.0 for modality in self.config.learning_modalities}
        
        # Visual learning indicators
        if 'visual_preference' in student_data.columns:
            style_scores['visual'] = student_data['visual_preference'].mean()
        
        if 'diagram_comprehension' in student_data.columns:
            style_scores['visual'] += student_data['diagram_comprehension'].mean() * 0.5
        
        # Auditory learning indicators
        if 'audio_preference' in student_data.columns:
            style_scores['auditory'] = student_data['audio_preference'].mean()
        
        if 'verbal_instruction_comprehension' in student_data.columns:
            style_scores['auditory'] += student_data['verbal_instruction_comprehension'].mean() * 0.5
        
        # Kinesthetic learning indicators
        if 'hands_on_preference' in student_data.columns:
            style_scores['kinesthetic'] = student_data['hands_on_preference'].mean()
        
        if 'physical_activity_engagement' in student_data.columns:
            style_scores['kinesthetic'] += student_data['physical_activity_engagement'].mean() * 0.5
        
        # Reading learning indicators
        if 'reading_preference' in student_data.columns:
            style_scores['reading'] = student_data['reading_preference'].mean()
        
        if 'text_comprehension' in student_data.columns:
            style_scores['reading'] += student_data['text_comprehension'].mean() * 0.5
        
        # Social learning indicators
        if 'group_work_preference' in student_data.columns:
            style_scores['social'] = student_data['group_work_preference'].mean()
        
        if 'peer_learning_effectiveness' in student_data.columns:
            style_scores['social'] += student_data['peer_learning_effectiveness'].mean() * 0.5
        
        # Normalize scores
        total_score = sum(style_scores.values())
        if total_score > 0:
            style_scores = {k: v / total_score for k, v in style_scores.items()}
        
        # Determine primary and secondary learning styles
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_styles[0][0]
        secondary_style = sorted_styles[1][0] if len(sorted_styles) > 1 else None
        
        analysis_result = {
            'style_scores': style_scores,
            'primary_style': primary_style,
            'secondary_style': secondary_style,
            'style_diversity': self._calculate_style_diversity(style_scores),
            'recommendations': self._generate_style_recommendations(style_scores)
        }
        
        logger.info(f"Learning style analysis complete. Primary style: {primary_style}")
        return analysis_result
    
    def _calculate_style_diversity(self, style_scores: Dict[str, float]) -> float:
        """Calculate the diversity of learning style preferences."""
        # Use entropy to measure diversity
        scores = np.array(list(style_scores.values()))
        scores = scores[scores > 0]  # Remove zero scores
        if len(scores) == 0:
            return 0.0
        
        # Normalize scores
        scores = scores / scores.sum()
        entropy = -np.sum(scores * np.log2(scores + 1e-10))
        max_entropy = np.log2(len(scores))
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _generate_style_recommendations(self, style_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on learning style analysis."""
        recommendations = []
        
        # Primary style recommendations
        primary_style = max(style_scores.items(), key=lambda x: x[1])[0]
        
        if primary_style == 'visual':
            recommendations.extend([
                'Use diagrams, charts, and visual aids',
                'Incorporate videos and infographics',
                'Provide visual summaries of concepts',
                'Use color coding for organization'
            ])
        elif primary_style == 'auditory':
            recommendations.extend([
                'Provide audio explanations',
                'Use verbal instructions and discussions',
                'Incorporate podcasts and audio content',
                'Encourage verbal repetition and explanation'
            ])
        elif primary_style == 'kinesthetic':
            recommendations.extend([
                'Include hands-on activities and experiments',
                'Use physical manipulatives',
                'Incorporate movement and physical engagement',
                'Provide real-world application opportunities'
            ])
        elif primary_style == 'reading':
            recommendations.extend([
                'Provide comprehensive written materials',
                'Use textbooks and articles',
                'Encourage note-taking and writing',
                'Provide reading assignments and summaries'
            ])
        elif primary_style == 'social':
            recommendations.extend([
                'Facilitate group discussions and projects',
                'Use peer teaching and collaboration',
                'Incorporate team-based learning activities',
                'Provide opportunities for peer feedback'
            ])
        
        # Balanced learning recommendations
        if self._calculate_style_diversity(style_scores) > 0.7:
            recommendations.append('Consider incorporating multiple learning modalities for balanced development')
        
        return recommendations

class ContentAdaptationEngine:
    """Engine for adapting content based on student needs and preferences."""
    
    def __init__(self, config: AdaptiveLearningConfig):
        self.config = config
        self.content_database = {}
        self.adaptation_rules = self._load_adaptation_rules()
        
    def adapt_content(self, content: Dict[str, Any], student_profile: Dict[str, Any],
                     performance_history: pd.DataFrame, learning_style: Dict[str, float]) -> Dict[str, Any]:
        """Adapt content based on student characteristics and performance."""
        logger.info("Adapting content for student...")
        
        adapted_content = content.copy()
        
        # Difficulty adaptation
        adapted_content = self._adapt_difficulty(adapted_content, student_profile, performance_history)
        
        # Format adaptation based on learning style
        adapted_content = self._adapt_format(adapted_content, learning_style)
        
        # Pacing adaptation
        adapted_content = self._adapt_pacing(adapted_content, student_profile, performance_history)
        
        # Content variety adaptation
        adapted_content = self._adapt_variety(adapted_content, student_profile)
        
        # Accessibility adaptation
        adapted_content = self._adapt_accessibility(adapted_content, student_profile)
        
        logger.info("Content adaptation complete")
        return adapted_content
    
    def _adapt_difficulty(self, content: Dict[str, Any], student_profile: Dict[str, Any],
                         performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Adapt content difficulty based on student performance."""
        current_difficulty = content.get('difficulty', 0.5)
        
        # Calculate performance-based difficulty adjustment
        if not performance_history.empty:
            recent_performance = performance_history.tail(5)['score'].mean()
            performance_difficulty = self._performance_to_difficulty(recent_performance)
            
            # Weighted combination of current and performance-based difficulty
            target_difficulty = (current_difficulty * 0.3 + performance_difficulty * 0.7)
        else:
            target_difficulty = current_difficulty
        
        # Apply difficulty constraints
        target_difficulty = max(0.1, min(1.0, target_difficulty))
        
        # Adjust content elements based on difficulty
        if 'questions' in content:
            content['questions'] = self._adjust_question_difficulty(
                content['questions'], target_difficulty
            )
        
        if 'explanations' in content:
            content['explanations'] = self._adjust_explanation_difficulty(
                content['explanations'], target_difficulty
            )
        
        content['adapted_difficulty'] = target_difficulty
        return content
    
    def _performance_to_difficulty(self, performance: float) -> float:
        """Convert performance score to appropriate difficulty level."""
        # Inverse relationship: higher performance = higher difficulty
        if performance < 0.6:
            return 0.3  # Low difficulty for struggling students
        elif performance < 0.8:
            return 0.6  # Medium difficulty for average students
        else:
            return 0.9  # High difficulty for high-performing students
    
    def _adjust_question_difficulty(self, questions: List[Dict[str, Any]], target_difficulty: float) -> List[Dict[str, Any]]:
        """Adjust question difficulty based on target difficulty."""
        adapted_questions = []
        
        for question in questions:
            adapted_question = question.copy()
            
            # Adjust question complexity
            if target_difficulty < 0.4:
                # Simplify questions
                if 'hints' not in adapted_question:
                    adapted_question['hints'] = ['Consider the basic concept', 'Think step by step']
                adapted_question['time_limit'] = adapted_question.get('time_limit', 60) * 1.5
            elif target_difficulty > 0.8:
                # Make questions more challenging
                if 'hints' in adapted_question:
                    adapted_question['hints'] = adapted_question['hints'][:1]  # Fewer hints
                adapted_question['time_limit'] = adapted_question.get('time_limit', 60) * 0.8
            
            adapted_questions.append(adapted_question)
        
        return adapted_questions
    
    def _adjust_explanation_difficulty(self, explanations: List[Dict[str, Any]], target_difficulty: float) -> List[Dict[str, Any]]:
        """Adjust explanation complexity based on target difficulty."""
        adapted_explanations = []
        
        for explanation in explanations:
            adapted_explanation = explanation.copy()
            
            if target_difficulty < 0.4:
                # Simplify explanations
                adapted_explanation['detail_level'] = 'basic'
                if 'examples' in adapted_explanation:
                    adapted_explanation['examples'] = adapted_explanation['examples'][:2]  # Fewer examples
            elif target_difficulty > 0.8:
                # Increase explanation complexity
                adapted_explanation['detail_level'] = 'advanced'
                if 'examples' in adapted_explanation:
                    adapted_explanation['examples'].extend(['Advanced application example'])
            
            adapted_explanations.append(adapted_explanation)
        
        return adapted_explanations
    
    def _adapt_format(self, content: Dict[str, Any], learning_style: Dict[str, float]) -> Dict[str, Any]:
        """Adapt content format based on learning style preferences."""
        adapted_content = content.copy()
        
        # Determine preferred format based on learning style
        primary_style = max(learning_style.items(), key=lambda x: x[1])[0]
        
        if primary_style == 'visual':
            # Enhance visual elements
            if 'images' not in adapted_content:
                adapted_content['images'] = ['Concept diagram', 'Process flowchart']
            if 'videos' in adapted_content:
                adapted_content['videos'] = adapted_content['videos'][:2]  # Prioritize videos
        
        elif primary_style == 'auditory':
            # Enhance audio elements
            if 'audio_narration' not in adapted_content:
                adapted_content['audio_narration'] = True
            if 'podcasts' not in adapted_content:
                adapted_content['podcasts'] = ['Related podcast episode']
        
        elif primary_style == 'kinesthetic':
            # Enhance interactive elements
            if 'interactive_elements' not in adapted_content:
                adapted_content['interactive_elements'] = ['Drag and drop', 'Simulation']
            if 'hands_on_activities' not in adapted_content:
                adapted_content['hands_on_activities'] = ['Physical experiment', 'Model building']
        
        elif primary_style == 'reading':
            # Enhance text-based elements
            if 'detailed_text' not in adapted_content:
                adapted_content['detailed_text'] = True
            if 'reading_materials' not in adapted_content:
                adapted_content['reading_materials'] = ['Comprehensive article', 'Chapter summary']
        
        elif primary_style == 'social':
            # Enhance collaborative elements
            if 'group_activities' not in adapted_content:
                adapted_content['group_activities'] = ['Peer discussion', 'Team project']
            if 'peer_feedback' not in adapted_content:
                adapted_content['peer_feedback'] = True
        
        return adapted_content
    
    def _adapt_pacing(self, content: Dict[str, Any], student_profile: Dict[str, Any],
                      performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Adapt content pacing based on student characteristics."""
        adapted_content = content.copy()
        
        # Analyze student's learning pace
        if not performance_history.empty:
            completion_times = performance_history.get('completion_time', [])
            if completion_times:
                avg_completion_time = np.mean(completion_times)
                pace_factor = self._calculate_pace_factor(avg_completion_time)
            else:
                pace_factor = 1.0
        else:
            pace_factor = 1.0
        
        # Adjust pacing elements
        if 'estimated_duration' in adapted_content:
            adapted_content['estimated_duration'] = int(
                adapted_content['estimated_duration'] * pace_factor
            )
        
        if 'time_limits' in adapted_content:
            adapted_content['time_limits'] = {
                k: int(v * pace_factor) for k, v in adapted_content['time_limits'].items()
            }
        
        adapted_content['pace_factor'] = pace_factor
        return adapted_content
    
    def _calculate_pace_factor(self, avg_completion_time: float) -> float:
        """Calculate pacing adjustment factor based on completion time."""
        # Normalize completion time (assuming 60 minutes is standard)
        standard_time = 60.0
        normalized_time = avg_completion_time / standard_time
        
        if normalized_time < 0.7:
            return 0.8  # Faster pace for quick learners
        elif normalized_time > 1.3:
            return 1.3  # Slower pace for slower learners
        else:
            return 1.0  # Standard pace
    
    def _adapt_variety(self, content: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt content variety based on student preferences."""
        adapted_content = content.copy()
        
        # Check student's preference for variety
        variety_preference = student_profile.get('content_variety_preference', 0.5)
        
        if variety_preference > 0.7:
            # High variety preference
            if 'alternative_formats' not in adapted_content:
                adapted_content['alternative_formats'] = [
                    'Video explanation', 'Interactive simulation', 'Text summary'
                ]
            if 'bonus_materials' not in adapted_content:
                adapted_content['bonus_materials'] = ['Advanced topic', 'Related concept']
        
        elif variety_preference < 0.3:
            # Low variety preference - focus on core content
            if 'alternative_formats' in adapted_content:
                adapted_content['alternative_formats'] = adapted_content['alternative_formats'][:1]
            if 'bonus_materials' in adapted_content:
                adapted_content['bonus_materials'] = []
        
        return adapted_content
    
    def _adapt_accessibility(self, content: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt content for accessibility needs."""
        adapted_content = content.copy()
        
        # Check for accessibility requirements
        accessibility_needs = student_profile.get('accessibility_needs', [])
        
        if 'visual_impairment' in accessibility_needs:
            # Add audio descriptions and text alternatives
            if 'audio_descriptions' not in adapted_content:
                adapted_content['audio_descriptions'] = True
            if 'text_alternatives' not in adapted_content:
                adapted_content['text_alternatives'] = True
        
        if 'hearing_impairment' in accessibility_needs:
            # Add captions and text transcripts
            if 'captions' not in adapted_content:
                adapted_content['captions'] = True
            if 'transcripts' not in adapted_content:
                adapted_content['transcripts'] = True
        
        if 'mobility_impairment' in accessibility_needs:
            # Ensure keyboard navigation and voice control
            if 'keyboard_navigation' not in adapted_content:
                adapted_content['keyboard_navigation'] = True
            if 'voice_control' not in adapted_content:
                adapted_content['voice_control'] = True
        
        return adapted_content
    
    def _load_adaptation_rules(self) -> Dict[str, Any]:
        """Load content adaptation rules from configuration."""
        return {
            'difficulty_scaling': {
                'low': {'hint_count': 3, 'time_multiplier': 1.5, 'example_count': 3},
                'medium': {'hint_count': 2, 'time_multiplier': 1.0, 'example_count': 2},
                'high': {'hint_count': 1, 'time_multiplier': 0.8, 'example_count': 1}
            },
            'format_preferences': {
                'visual': ['diagrams', 'videos', 'infographics'],
                'auditory': ['audio', 'podcasts', 'discussions'],
                'kinesthetic': ['interactive', 'hands_on', 'simulations'],
                'reading': ['text', 'articles', 'summaries'],
                'social': ['group_work', 'peer_learning', 'collaboration']
            }
        }

class LearningPathGenerator:
    """Generates personalized learning paths for students."""
    
    def __init__(self, config: AdaptiveLearningConfig):
        self.config = config
        self.content_graph = {}
        self.prerequisite_map = {}
        
    def generate_learning_path(self, student_id: str, subject: str, 
                              learning_objectives: List[str], student_profile: Dict[str, Any],
                              performance_history: pd.DataFrame) -> LearningPath:
        """Generate a personalized learning path for a student."""
        logger.info(f"Generating learning path for student {student_id} in {subject}")
        
        # Create learning path
        learning_path = LearningPath(student_id, subject, learning_objectives)
        
        # Analyze student characteristics
        learning_style_analyzer = LearningStyleAnalyzer(self.config)
        learning_style = learning_style_analyzer.analyze_learning_style(performance_history)
        
        # Generate content sequence
        content_sequence = self._generate_content_sequence(
            learning_objectives, student_profile, learning_style, performance_history
        )
        
        # Create learning path nodes
        for content_item in content_sequence:
            node = LearningPathNode(
                content_id=content_item['id'],
                content_type=content_item['type'],
                difficulty=content_item['difficulty'],
                prerequisites=content_item.get('prerequisites', []),
                estimated_duration=content_item.get('estimated_duration', 30)
            )
            learning_path.add_node(node)
        
        logger.info(f"Learning path generated with {len(content_sequence)} nodes")
        return learning_path
    
    def _generate_content_sequence(self, learning_objectives: List[str], 
                                  student_profile: Dict[str, Any],
                                  learning_style: Dict[str, Any],
                                  performance_history: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate the sequence of content items for the learning path."""
        content_sequence = []
        
        # Map learning objectives to content items
        for objective in learning_objectives:
            objective_content = self._get_content_for_objective(
                objective, student_profile, learning_style
            )
            content_sequence.extend(objective_content)
        
        # Sort by prerequisites and difficulty
        content_sequence = self._sort_content_by_prerequisites(content_sequence)
        
        # Optimize sequence based on student characteristics
        content_sequence = self._optimize_sequence(content_sequence, student_profile, performance_history)
        
        # Limit path length
        if len(content_sequence) > self.config.max_path_length:
            content_sequence = content_sequence[:self.config.max_path_length]
        
        return content_sequence
    
    def _get_content_for_objective(self, objective: str, student_profile: Dict[str, Any],
                                  learning_style: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get content items for a specific learning objective."""
        # This would query the content database
        # For now, return placeholder content
        primary_style = learning_style.get('primary_style', 'visual')
        
        content_items = [
            {
                'id': f'{objective}_intro_{primary_style}',
                'type': 'introduction',
                'difficulty': 0.3,
                'estimated_duration': 20,
                'modality': primary_style,
                'prerequisites': []
            },
            {
                'id': f'{objective}_core_{primary_style}',
                'type': 'core_content',
                'difficulty': 0.6,
                'estimated_duration': 45,
                'modality': primary_style,
                'prerequisites': [f'{objective}_intro_{primary_style}']
            },
            {
                'id': f'{objective}_practice_{primary_style}',
                'type': 'practice',
                'difficulty': 0.7,
                'estimated_duration': 30,
                'modality': primary_style,
                'prerequisites': [f'{objective}_core_{primary_style}']
            },
            {
                'id': f'{objective}_assessment_{primary_style}',
                'type': 'assessment',
                'difficulty': 0.8,
                'estimated_duration': 25,
                'modality': primary_style,
                'prerequisites': [f'{objective}_practice_{primary_style}']
            }
        ]
        
        return content_items
    
    def _sort_content_by_prerequisites(self, content_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort content items based on prerequisite relationships."""
        # Topological sort for prerequisites
        sorted_content = []
        visited = set()
        
        def visit(item):
            if item['id'] in visited:
                return
            
            # Visit prerequisites first
            for prereq_id in item.get('prerequisites', []):
                prereq_item = next((c for c in content_sequence if c['id'] == prereq_id), None)
                if prereq_item:
                    visit(prereq_item)
            
            visited.add(item['id'])
            sorted_content.append(item)
        
        for item in content_sequence:
            visit(item)
        
        return sorted_content
    
    def _optimize_sequence(self, content_sequence: List[Dict[str, Any]], 
                          student_profile: Dict[str, Any],
                          performance_history: pd.DataFrame) -> List[Dict[str, Any]]:
        """Optimize content sequence based on student characteristics."""
        optimized_sequence = content_sequence.copy()
        
        # Analyze performance patterns
        if not performance_history.empty:
            # Check for time-of-day preferences
            time_preferences = self._analyze_time_preferences(performance_history)
            
            # Check for content type preferences
            content_preferences = self._analyze_content_preferences(performance_history)
            
            # Reorder content based on preferences
            optimized_sequence = self._reorder_by_preferences(
                optimized_sequence, time_preferences, content_preferences
            )
        
        return optimized_sequence
    
    def _analyze_time_preferences(self, performance_history: pd.DataFrame) -> Dict[str, float]:
        """Analyze student's time-of-day performance preferences."""
        time_preferences = {
            'morning': 0.0,
            'afternoon': 0.0,
            'evening': 0.0
        }
        
        if 'timestamp' in performance_history.columns:
            performance_history['hour'] = pd.to_datetime(performance_history['timestamp']).dt.hour
            
            morning_scores = performance_history[performance_history['hour'].between(6, 12)]['score'].mean()
            afternoon_scores = performance_history[performance_history['hour'].between(12, 18)]['score'].mean()
            evening_scores = performance_history[performance_history['hour'].between(18, 22)]['score'].mean()
            
            time_preferences['morning'] = morning_scores if not pd.isna(morning_scores) else 0.5
            time_preferences['afternoon'] = afternoon_scores if not pd.isna(afternoon_scores) else 0.5
            time_preferences['evening'] = evening_scores if not pd.isna(evening_scores) else 0.5
        
        return time_preferences
    
    def _analyze_content_preferences(self, performance_history: pd.DataFrame) -> Dict[str, float]:
        """Analyze student's content type preferences based on performance."""
        content_preferences = {
            'introduction': 0.5,
            'core_content': 0.5,
            'practice': 0.5,
            'assessment': 0.5
        }
        
        if 'content_type' in performance_history.columns:
            for content_type in content_preferences.keys():
                type_scores = performance_history[
                    performance_history['content_type'] == content_type
                ]['score'].mean()
                if not pd.isna(type_scores):
                    content_preferences[content_type] = type_scores
        
        return content_preferences
    
    def _reorder_by_preferences(self, content_sequence: List[Dict[str, Any]],
                               time_preferences: Dict[str, float],
                               content_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Reorder content based on student preferences."""
        # Calculate preference scores for each content item
        for item in content_sequence:
            preference_score = 0.0
            
            # Content type preference
            content_type = item.get('type', 'core_content')
            preference_score += content_preferences.get(content_type, 0.5)
            
            # Modality preference (if available)
            modality = item.get('modality', 'visual')
            if modality in content_preferences:
                preference_score += content_preferences[modality] * 0.3
            
            item['preference_score'] = preference_score
        
        # Sort by preference score (descending)
        content_sequence.sort(key=lambda x: x.get('preference_score', 0.5), reverse=True)
        
        # Maintain prerequisite relationships
        content_sequence = self._sort_content_by_prerequisites(content_sequence)
        
        return content_sequence

class AdaptiveLearningEngine:
    """Main engine that orchestrates all adaptive learning components."""
    
    def __init__(self, config: AdaptiveLearningConfig):
        self.config = config
        self.learning_style_analyzer = LearningStyleAnalyzer(config)
        self.content_adaptation_engine = ContentAdaptationEngine(config)
        self.learning_path_generator = LearningPathGenerator(config)
        self.adaptation_history = []
        
    def create_personalized_learning_experience(self, student_id: str, subject: str,
                                              learning_objectives: List[str],
                                              student_profile: Dict[str, Any],
                                              performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Create a complete personalized learning experience for a student."""
        logger.info(f"Creating personalized learning experience for student {student_id}")
        
        # Analyze learning style
        learning_style = self.learning_style_analyzer.analyze_learning_style(performance_history)
        
        # Generate learning path
        learning_path = self.learning_path_generator.generate_learning_path(
            student_id, subject, learning_objectives, student_profile, performance_history
        )
        
        # Adapt content for current node
        current_node = learning_path.get_current_node()
        if current_node:
            adapted_content = self.content_adaptation_engine.adapt_content(
                self._get_content_by_id(current_node.content_id),
                student_profile,
                performance_history,
                learning_style['style_scores']
            )
        else:
            adapted_content = {}
        
        # Create learning experience
        learning_experience = {
            'student_id': student_id,
            'subject': subject,
            'learning_objectives': learning_objectives,
            'learning_path': learning_path.to_dict(),
            'current_content': adapted_content,
            'learning_style': learning_style,
            'recommendations': self._generate_learning_recommendations(
                learning_style, performance_history
            ),
            'progress_tracking': self._create_progress_tracking(learning_path, performance_history)
        }
        
        # Record adaptation
        self.adaptation_history.append({
            'timestamp': datetime.now().isoformat(),
            'student_id': student_id,
            'adaptation_type': 'learning_experience_creation',
            'details': learning_experience
        })
        
        logger.info("Personalized learning experience created successfully")
        return learning_experience
    
    def _get_content_by_id(self, content_id: str) -> Dict[str, Any]:
        """Get content by ID from the content database."""
        # This would query the actual content database
        # For now, return placeholder content
        return {
            'id': content_id,
            'title': f'Content for {content_id}',
            'type': 'core_content',
            'difficulty': 0.6,
            'estimated_duration': 30,
            'questions': [
                {'question': 'Sample question 1', 'difficulty': 0.5, 'time_limit': 60},
                {'question': 'Sample question 2', 'difficulty': 0.7, 'time_limit': 60}
            ],
            'explanations': [
                {'explanation': 'Sample explanation', 'detail_level': 'medium'}
            ]
        }
    
    def _generate_learning_recommendations(self, learning_style: Dict[str, Any],
                                         performance_history: pd.DataFrame) -> List[str]:
        """Generate learning recommendations based on style and performance."""
        recommendations = []
        
        # Style-based recommendations
        recommendations.extend(learning_style.get('recommendations', []))
        
        # Performance-based recommendations
        if not performance_history.empty:
            recent_performance = performance_history.tail(5)['score'].mean()
            
            if recent_performance < 0.6:
                recommendations.append('Consider reviewing foundational concepts before proceeding')
                recommendations.append('Take advantage of additional practice opportunities')
            elif recent_performance > 0.9:
                recommendations.append('You\'re performing excellently! Consider challenging yourself with advanced topics')
                recommendations.append('Help peers who might be struggling with the material')
        
        return recommendations
    
    def _create_progress_tracking(self, learning_path: LearningPath,
                                 performance_history: pd.DataFrame) -> Dict[str, Any]:
        """Create progress tracking information."""
        progress = {
            'overall_progress': learning_path.completion_percentage,
            'current_node': learning_path.current_node_index,
            'total_nodes': len(learning_path.nodes),
            'estimated_completion_time': learning_path.estimated_completion_time,
            'performance_trend': self._calculate_performance_trend(performance_history),
            'strengths': self._identify_strengths(performance_history),
            'areas_for_improvement': self._identify_improvement_areas(performance_history)
        }
        
        return progress
    
    def _calculate_performance_trend(self, performance_history: pd.DataFrame) -> str:
        """Calculate the trend in student performance."""
        if len(performance_history) < 3:
            return 'insufficient_data'
        
        recent_scores = performance_history.tail(3)['score'].values
        if len(recent_scores) >= 2:
            slope = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            
            if slope > 0.05:
                return 'improving'
            elif slope < -0.05:
                return 'declining'
            else:
                return 'stable'
        
        return 'insufficient_data'
    
    def _identify_strengths(self, performance_history: pd.DataFrame) -> List[str]:
        """Identify student's learning strengths."""
        strengths = []
        
        if not performance_history.empty:
            # Check for high performance areas
            if 'content_type' in performance_history.columns:
                for content_type in performance_history['content_type'].unique():
                    type_scores = performance_history[
                        performance_history['content_type'] == content_type
                    ]['score'].mean()
                    if type_scores > 0.8:
                        strengths.append(f'Strong performance in {content_type}')
            
            # Check for consistent performance
            if len(performance_history) >= 5:
                recent_scores = performance_history.tail(5)['score']
                if recent_scores.std() < 0.1:
                    strengths.append('Consistent performance')
        
        return strengths
    
    def _identify_improvement_areas(self, performance_history: pd.DataFrame) -> List[str]:
        """Identify areas where the student could improve."""
        improvement_areas = []
        
        if not performance_history.empty:
            # Check for low performance areas
            if 'content_type' in performance_history.columns:
                for content_type in performance_history['content_type'].unique():
                    type_scores = performance_history[
                        performance_history['content_type'] == content_type
                    ]['score'].mean()
                    if type_scores < 0.6:
                        improvement_areas.append(f'Need improvement in {content_type}')
            
            # Check for performance decline
            if len(performance_history) >= 3:
                recent_scores = performance_history.tail(3)['score']
                if recent_scores.iloc[-1] < recent_scores.iloc[0] - 0.1:
                    improvement_areas.append('Recent performance decline detected')
        
        return improvement_areas

# Example usage
if __name__ == "__main__":
    # Example configuration
    config = AdaptiveLearningConfig(
        max_path_length=15,
        min_path_length=5,
        branching_factor=3,
        difficulty_levels=5,
        content_variety=8
    )
    
    # Create adaptive learning engine
    adaptive_engine = AdaptiveLearningEngine(config)
    
    # Example student data
    student_profile = {
        'student_id': 'STU001',
        'grade_level': 10,
        'subject_preferences': ['math', 'science'],
        'accessibility_needs': [],
        'content_variety_preference': 0.7
    }
    
    # Example performance history
    performance_data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'score': [0.7, 0.8, 0.6, 0.9, 0.8, 0.7, 0.9, 0.8, 0.9, 0.9],
        'content_type': ['core_content'] * 10,
        'completion_time': [25, 30, 35, 20, 25, 30, 20, 25, 20, 20]
    }
    performance_history = pd.DataFrame(performance_data)
    
    # Create personalized learning experience
    learning_experience = adaptive_engine.create_personalized_learning_experience(
        student_id='STU001',
        subject='mathematics',
        learning_objectives=['algebraic_expressions', 'linear_equations'],
        student_profile=student_profile,
        performance_history=performance_history
    )
    
    logger.info("Adaptive learning engine created successfully!")
    logger.info(f"Generated learning path with {len(learning_experience['learning_path']['nodes'])} nodes")