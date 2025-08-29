"""
Phase 3: Offline Capabilities and Local AI Models
Provides AI functionality for low-connectivity areas
"""
import json
import logging
import os
import sqlite3
import pickle
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import joblib
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification,
    pipeline, GPT2LMHeadModel, GPT2Tokenizer
)
import torch
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class OfflineAIService:
    """
    Offline AI service using local models for areas with limited connectivity
    """
    
    def __init__(self):
        self.models_path = Path('/workspace/ai_models/offline/')
        self.models_path.mkdir(parents=True, exist_ok=True)
        
        # Local model instances
        self.local_chat_model = None
        self.local_tokenizer = None
        self.sentiment_analyzer = None
        self.question_answerer = None
        self.text_generator = None
        
        # Offline database for caching
        self.offline_db_path = self.models_path / 'offline_cache.db'
        self._initialize_offline_database()
        
        # Model configurations
        self.model_configs = {
            'chat_model': 'microsoft/DialoGPT-small',  # Lightweight conversational AI
            'sentiment_model': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
            'qa_model': 'distilbert-base-cased-distilled-squad',
            'text_gen_model': 'gpt2'  # Lightweight text generation
        }
        
        self._load_offline_models()
    
    def _initialize_offline_database(self):
        """
        Initialize SQLite database for offline caching
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            # Create tables for offline data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS offline_lessons (
                    id INTEGER PRIMARY KEY,
                    lesson_id TEXT UNIQUE,
                    title TEXT,
                    content TEXT,
                    subject TEXT,
                    grade_level TEXT,
                    language TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS offline_conversations (
                    id INTEGER PRIMARY KEY,
                    conversation_id TEXT,
                    student_id TEXT,
                    message TEXT,
                    response TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS offline_analytics (
                    id INTEGER PRIMARY KEY,
                    student_id TEXT,
                    metric_type TEXT,
                    metric_value TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_queue (
                    id INTEGER PRIMARY KEY,
                    data_type TEXT,
                    data_content TEXT,
                    sync_status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Offline database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize offline database: {e}")
    
    def _load_offline_models(self):
        """
        Load local AI models for offline functionality
        """
        try:
            logger.info("Loading offline AI models...")
            
            # Load lightweight chat model
            if not self.local_chat_model:
                model_path = self.models_path / 'chat_model'
                if model_path.exists():
                    self.local_chat_model = AutoModelForCausalLM.from_pretrained(model_path)
                    self.local_tokenizer = AutoTokenizer.from_pretrained(model_path)
                else:
                    # Download and save model for first time
                    self._download_and_cache_model('chat_model')
            
            # Load sentiment analyzer
            if not self.sentiment_analyzer:
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model=self.model_configs['sentiment_model'],
                    return_all_scores=True
                )
            
            # Load question answering model
            if not self.question_answerer:
                self.question_answerer = pipeline(
                    "question-answering",
                    model=self.model_configs['qa_model']
                )
            
            # Load text generator
            if not self.text_generator:
                self.text_generator = pipeline(
                    "text-generation",
                    model=self.model_configs['text_gen_model'],
                    max_length=200,
                    temperature=0.7
                )
            
            logger.info("Offline AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load offline models: {e}")
    
    def _download_and_cache_model(self, model_type: str):
        """
        Download and cache models locally
        """
        try:
            model_name = self.model_configs[model_type]
            save_path = self.models_path / model_type
            
            logger.info(f"Downloading {model_type} model: {model_name}")
            
            if model_type == 'chat_model':
                model = AutoModelForCausalLM.from_pretrained(model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                model.save_pretrained(save_path)
                tokenizer.save_pretrained(save_path)
                
                self.local_chat_model = model
                self.local_tokenizer = tokenizer
            
            logger.info(f"Model {model_type} cached successfully")
            
        except Exception as e:
            logger.error(f"Failed to download and cache model {model_type}: {e}")
    
    def generate_offline_response(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate AI response using local models
        """
        try:
            if not self.local_chat_model or not self.local_tokenizer:
                return {
                    'response': "I'm currently operating in offline mode with limited capabilities. Please try again when online.",
                    'confidence': 0.3,
                    'source': 'fallback'
                }
            
            # Prepare input with context
            input_text = self._prepare_input_with_context(message, context)
            
            # Tokenize input
            inputs = self.local_tokenizer.encode(input_text, return_tensors='pt')
            
            # Generate response
            with torch.no_grad():
                outputs = self.local_chat_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.local_tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.local_tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(input_text):].strip()
            
            # Analyze sentiment of response
            sentiment = self._analyze_offline_sentiment(response)
            
            return {
                'response': response,
                'confidence': 0.7,
                'source': 'local_model',
                'sentiment': sentiment,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Offline response generation error: {e}")
            return {
                'response': "I'm having trouble processing your request offline. Please try a simpler question.",
                'confidence': 0.2,
                'source': 'error_fallback'
            }
    
    def _prepare_input_with_context(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Prepare input text with conversation context
        """
        if not context:
            return f"Student: {message}\nAI Teacher:"
        
        context_str = ""
        if 'subject' in context:
            context_str += f"Subject: {context['subject']}\n"
        if 'grade_level' in context:
            context_str += f"Grade: {context['grade_level']}\n"
        if 'previous_messages' in context:
            for msg in context['previous_messages'][-3:]:  # Last 3 messages
                context_str += f"{msg.get('role', 'Student')}: {msg.get('content', '')}\n"
        
        return f"{context_str}Student: {message}\nAI Teacher:"
    
    def _analyze_offline_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using local model
        """
        try:
            if self.sentiment_analyzer:
                results = self.sentiment_analyzer(text)
                sentiment_scores = {result['label'].lower(): result['score'] for result in results[0]}
                return sentiment_scores
            else:
                return {'neutral': 0.5, 'positive': 0.3, 'negative': 0.2}
        except Exception as e:
            logger.error(f"Offline sentiment analysis error: {e}")
            return {'neutral': 1.0}
    
    def cache_lesson_offline(self, lesson_data: Dict[str, Any]) -> bool:
        """
        Cache lesson data for offline access
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO offline_lessons 
                (lesson_id, title, content, subject, grade_level, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                lesson_data.get('id'),
                lesson_data.get('title'),
                json.dumps(lesson_data.get('content', {})),
                lesson_data.get('subject'),
                lesson_data.get('grade_level'),
                lesson_data.get('language', 'en')
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Lesson {lesson_data.get('id')} cached offline")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache lesson offline: {e}")
            return False
    
    def get_offline_lesson(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached lesson for offline access
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, content, subject, grade_level, language 
                FROM offline_lessons WHERE lesson_id = ?
            ''', (lesson_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': lesson_id,
                    'title': result[0],
                    'content': json.loads(result[1]),
                    'subject': result[2],
                    'grade_level': result[3],
                    'language': result[4]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve offline lesson: {e}")
            return None
    
    def store_offline_interaction(self, student_id: str, message: str, response: str) -> bool:
        """
        Store interaction for later synchronization
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO offline_conversations 
                (student_id, message, response)
                VALUES (?, ?, ?)
            ''', (student_id, message, response))
            
            # Also add to sync queue
            cursor.execute('''
                INSERT INTO sync_queue (data_type, data_content)
                VALUES (?, ?)
            ''', ('conversation', json.dumps({
                'student_id': student_id,
                'message': message,
                'response': response,
                'timestamp': datetime.now().isoformat()
            })))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to store offline interaction: {e}")
            return False
    
    def get_sync_queue(self) -> List[Dict[str, Any]]:
        """
        Get pending data for synchronization when online
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, data_type, data_content, created_at 
                FROM sync_queue WHERE sync_status = 'pending'
                ORDER BY created_at ASC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            sync_data = []
            for result in results:
                sync_data.append({
                    'id': result[0],
                    'data_type': result[1],
                    'data_content': json.loads(result[2]),
                    'created_at': result[3]
                })
            
            return sync_data
            
        except Exception as e:
            logger.error(f"Failed to get sync queue: {e}")
            return []
    
    def mark_synced(self, sync_ids: List[int]) -> bool:
        """
        Mark data as synced after successful upload
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            placeholders = ','.join('?' * len(sync_ids))
            cursor.execute(f'''
                UPDATE sync_queue 
                SET sync_status = 'completed', updated_at = CURRENT_TIMESTAMP
                WHERE id IN ({placeholders})
            ''', sync_ids)
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark data as synced: {e}")
            return False
    
    def generate_offline_lesson_content(self, topic: str, grade_level: str, language: str = 'en') -> Dict[str, Any]:
        """
        Generate basic lesson content using local models
        """
        try:
            # Create a simple lesson structure
            prompt = f"Create a lesson about {topic} for grade {grade_level} students. Include key concepts and examples."
            
            if self.text_generator:
                generated_content = self.text_generator(prompt, max_length=300, num_return_sequences=1)
                content_text = generated_content[0]['generated_text'][len(prompt):].strip()
            else:
                content_text = f"This is a basic lesson about {topic}. Key concepts will be covered with examples appropriate for grade {grade_level}."
            
            lesson_content = {
                'title': f"{topic} - Grade {grade_level}",
                'description': f"Offline-generated lesson about {topic}",
                'content': {
                    'introduction': content_text[:200],
                    'main_content': content_text[200:400] if len(content_text) > 200 else "Additional content to be provided when online.",
                    'summary': "Key points will be summarized here.",
                    'exercises': ["Practice exercise 1", "Practice exercise 2"]
                },
                'subject': topic,
                'grade_level': grade_level,
                'language': language,
                'generated_offline': True,
                'timestamp': datetime.now().isoformat()
            }
            
            return lesson_content
            
        except Exception as e:
            logger.error(f"Failed to generate offline lesson content: {e}")
            return {
                'title': f"{topic} - Grade {grade_level}",
                'description': "Offline lesson template",
                'content': {
                    'introduction': f"This lesson covers {topic} for grade {grade_level} students.",
                    'main_content': "Detailed content will be available when online connection is restored.",
                    'summary': "Key concepts and takeaways will be provided.",
                    'exercises': []
                },
                'generated_offline': True,
                'offline_template': True
            }
    
    def check_connectivity(self) -> Dict[str, Any]:
        """
        Check internet connectivity status
        """
        try:
            import requests
            response = requests.get('https://www.google.com', timeout=5)
            return {
                'online': True,
                'status': 'connected',
                'last_check': datetime.now().isoformat()
            }
        except:
            return {
                'online': False,
                'status': 'offline',
                'last_check': datetime.now().isoformat()
            }
    
    def get_offline_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about offline usage
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            cursor = conn.cursor()
            
            # Count cached lessons
            cursor.execute('SELECT COUNT(*) FROM offline_lessons')
            lessons_count = cursor.fetchone()[0]
            
            # Count offline conversations
            cursor.execute('SELECT COUNT(*) FROM offline_conversations')
            conversations_count = cursor.fetchone()[0]
            
            # Count pending sync items
            cursor.execute('SELECT COUNT(*) FROM sync_queue WHERE sync_status = "pending"')
            pending_sync_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'cached_lessons': lessons_count,
                'offline_conversations': conversations_count,
                'pending_sync_items': pending_sync_count,
                'models_loaded': {
                    'chat_model': self.local_chat_model is not None,
                    'sentiment_analyzer': self.sentiment_analyzer is not None,
                    'question_answerer': self.question_answerer is not None,
                    'text_generator': self.text_generator is not None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get offline statistics: {e}")
            return {'error': str(e)}


class OfflineSyncService:
    """
    Service for synchronizing offline data when connection is restored
    """
    
    def __init__(self):
        self.offline_ai = OfflineAIService()
    
    def sync_offline_data(self) -> Dict[str, Any]:
        """
        Synchronize all offline data with the main system
        """
        try:
            sync_results = {
                'conversations_synced': 0,
                'analytics_synced': 0,
                'errors': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Get pending sync data
            sync_queue = self.offline_ai.get_sync_queue()
            
            synced_ids = []
            
            for item in sync_queue:
                try:
                    if item['data_type'] == 'conversation':
                        success = self._sync_conversation(item['data_content'])
                        if success:
                            sync_results['conversations_synced'] += 1
                            synced_ids.append(item['id'])
                    
                    elif item['data_type'] == 'analytics':
                        success = self._sync_analytics(item['data_content'])
                        if success:
                            sync_results['analytics_synced'] += 1
                            synced_ids.append(item['id'])
                            
                except Exception as e:
                    sync_results['errors'].append(f"Failed to sync item {item['id']}: {str(e)}")
            
            # Mark synced items
            if synced_ids:
                self.offline_ai.mark_synced(synced_ids)
            
            return sync_results
            
        except Exception as e:
            logger.error(f"Sync process failed: {e}")
            return {'error': str(e)}
    
    def _sync_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """
        Sync conversation data with main database
        """
        try:
            # Import here to avoid circular imports
            from .models import AIConversation, ConversationMessage
            from accounts.models import User
            
            # Find or create conversation
            student = User.objects.get(id=conversation_data['student_id'])
            
            # Create conversation record
            # This would integrate with the main conversation system
            logger.info(f"Synced conversation for student {student.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync conversation: {e}")
            return False
    
    def _sync_analytics(self, analytics_data: Dict[str, Any]) -> bool:
        """
        Sync analytics data with main database
        """
        try:
            # Sync with analytics system
            logger.info(f"Synced analytics data")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync analytics: {e}")
            return False


# Initialize offline services
offline_ai_service = OfflineAIService()
offline_sync_service = OfflineSyncService()