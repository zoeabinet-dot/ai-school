import { apiService } from './api';
import { 
  AILesson, 
  AIConversation, 
  ConversationMessage,
  PaginatedResponse 
} from '../types';

// AI Teacher API Service
export class AITeacherApiService {
  // AI Lessons
  static async getAILessons(params?: {
    page?: number;
    page_size?: number;
    subject?: string;
    grade_level?: number;
    difficulty_level?: string;
  }): Promise<PaginatedResponse<AILesson>> {
    return apiService.get('/ai-teacher/lessons/', { params });
  }

  static async getAILesson(id: number): Promise<AILesson> {
    return apiService.get(`/ai-teacher/lessons/${id}/`);
  }

  static async createAILesson(data: Partial<AILesson>): Promise<AILesson> {
    return apiService.post('/ai-teacher/lessons/', data);
  }

  static async updateAILesson(id: number, data: Partial<AILesson>): Promise<AILesson> {
    return apiService.put(`/ai-teacher/lessons/${id}/`, data);
  }

  static async deleteAILesson(id: number): Promise<void> {
    return apiService.delete(`/ai-teacher/lessons/${id}/`);
  }

  // Generate AI Lesson
  static async generateAILesson(prompt: string): Promise<AILesson> {
    return apiService.post('/ai-teacher/generate-lesson/', { prompt });
  }

  // AI Conversations
  static async getConversations(studentId?: number): Promise<AIConversation[]> {
    const params = studentId ? { student_id: studentId } : {};
    return apiService.get('/ai-teacher/conversations/', { params });
  }

  static async getConversation(id: number): Promise<AIConversation> {
    return apiService.get(`/ai-teacher/conversations/${id}/`);
  }

  static async createConversation(data: Partial<AIConversation>): Promise<AIConversation> {
    return apiService.post('/ai-teacher/conversations/', data);
  }

  static async updateConversation(id: number, data: Partial<AIConversation>): Promise<AIConversation> {
    return apiService.put(`/ai-teacher/conversations/${id}/`, data);
  }

  static async deleteConversation(id: number): Promise<void> {
    return apiService.delete(`/ai-teacher/conversations/${id}/`);
  }

  // Conversation Messages
  static async getConversationMessages(conversationId: number): Promise<ConversationMessage[]> {
    return apiService.get(`/ai-teacher/conversations/${conversationId}/messages/`);
  }

  static async sendMessage(conversationId: number, data: Partial<ConversationMessage>): Promise<ConversationMessage> {
    return apiService.post(`/ai-teacher/conversations/${conversationId}/messages/`, data);
  }

  // Speech Processing
  static async speechToText(audioFile: File): Promise<{ text: string }> {
    const formData = new FormData();
    formData.append('audio', audioFile);
    return apiService.post('/ai-teacher/speech-to-text/', formData);
  }

  static async textToSpeech(text: string, voice?: string): Promise<{ audio_url: string }> {
    return apiService.post('/ai-teacher/text-to-speech/', { text, voice });
  }

  // AI Recommendations
  static async getRecommendations(studentId: number): Promise<any[]> {
    return apiService.get(`/ai-teacher/recommendations/${studentId}/`);
  }

  static async generateRecommendations(studentId: number): Promise<any[]> {
    return apiService.post(`/ai-teacher/recommendations/${studentId}/generate/`);
  }

  // Behavioral Analysis
  static async analyzeBehavior(studentId: number, data: any): Promise<any> {
    return apiService.post(`/ai-teacher/behavior-analysis/${studentId}/`, data);
  }

  static async getBehaviorReport(studentId: number, dateRange?: string): Promise<any> {
    const params = dateRange ? { date_range: dateRange } : {};
    return apiService.get(`/ai-teacher/behavior-analysis/${studentId}/report/`, { params });
  }

  // AI Model Management
  static async getAIModels(): Promise<any[]> {
    return apiService.get('/ai-teacher/models/');
  }

  static async getAIModel(id: string): Promise<any> {
    return apiService.get(`/ai-teacher/models/${id}/`);
  }

  static async trainAIModel(modelId: string, data: any): Promise<any> {
    return apiService.post(`/ai-teacher/models/${modelId}/train/`, data);
  }

  static async deployAIModel(modelId: string): Promise<any> {
    return apiService.post(`/ai-teacher/models/${modelId}/deploy/`);
  }

  // AI Insights
  static async getAIInsights(studentId: number): Promise<any> {
    return apiService.get(`/ai-teacher/insights/${studentId}/`);
  }

  static async generateAIInsights(studentId: number): Promise<any> {
    return apiService.post(`/ai-teacher/insights/${studentId}/generate/`);
  }
}

export default AITeacherApiService;