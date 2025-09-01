import { apiService } from './api';

function normalizeResponse(res: any) {
  if (res && typeof res === 'object') {
    if (res.data && Object.prototype.hasOwnProperty.call(res.data, 'results')) return res;
    if (res.data) return res.data;
  }
  return res;
}
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
  const res = await apiService.get('/ai-teacher/lessons/', { params });
  return normalizeResponse(res);
  }

  static async getAILesson(id: number): Promise<AILesson> {
  const res = await apiService.get(`/ai-teacher/lessons/${id}/`);
  return normalizeResponse(res);
  }

  static async createAILesson(data: Partial<AILesson>): Promise<AILesson> {
  const res = await apiService.post('/ai-teacher/lessons/', data);
  return normalizeResponse(res);
  }

  static async updateAILesson(id: number, data: Partial<AILesson>): Promise<AILesson> {
  const res = await apiService.put(`/ai-teacher/lessons/${id}/`, data);
  return normalizeResponse(res);
  }

  static async deleteAILesson(id: number): Promise<void> {
  const res = await apiService.delete(`/ai-teacher/lessons/${id}/`);
  return normalizeResponse(res);
  }

  // Generate AI Lesson
  static async generateAILesson(prompt: string): Promise<AILesson> {
  const res = await apiService.post('/ai-teacher/generate-lesson/', { prompt });
  return normalizeResponse(res);
  }

  // AI Conversations
  static async getConversations(studentId?: number): Promise<AIConversation[]> {
    const params = studentId ? { student_id: studentId } : {};
  const res = await apiService.get('/ai-teacher/conversations/', { params });
  return normalizeResponse(res);
  }

  static async getConversation(id: number): Promise<AIConversation> {
  const res = await apiService.get(`/ai-teacher/conversations/${id}/`);
  return normalizeResponse(res);
  }

  static async createConversation(data: any): Promise<AIConversation> {
  const res = await apiService.post('/ai-teacher/conversations/', data);
  return normalizeResponse(res);
  }

  static async updateConversation(id: number, data: Partial<AIConversation>): Promise<AIConversation> {
  const res = await apiService.put(`/ai-teacher/conversations/${id}/`, data);
  return normalizeResponse(res);
  }

  static async deleteConversation(id: number): Promise<void> {
  const res = await apiService.delete(`/ai-teacher/conversations/${id}/`);
  return normalizeResponse(res);
  }

  // Conversation Messages
  static async getConversationMessages(conversationId: number): Promise<ConversationMessage[]> {
  const res = await apiService.get(`/ai-teacher/conversations/${conversationId}/messages/`);
  return normalizeResponse(res);
  }

  static async sendMessage(conversationId: number, data: Partial<ConversationMessage>): Promise<ConversationMessage> {
  const res = await apiService.post(`/ai-teacher/conversations/${conversationId}/messages/`, data);
  return normalizeResponse(res);
  }

  // Speech Processing
  static async speechToText(audioFile: File): Promise<{ text: string }> {
    const formData = new FormData();
    formData.append('audio', audioFile);
  const res = await apiService.post('/ai-teacher/speech-to-text/', formData);
  return normalizeResponse(res);
  }

  static async textToSpeech(text: string, voice?: string): Promise<{ audio_url: string }> {
  const res = await apiService.post('/ai-teacher/text-to-speech/', { text, voice });
  return normalizeResponse(res);
  }

  // AI Recommendations
  static async getRecommendations(studentId: number): Promise<any[]> {
  const res = await apiService.get(`/ai-teacher/recommendations/${studentId}/`);
  return normalizeResponse(res);
  }

  static async generateRecommendations(studentId: number): Promise<any[]> {
  const res = await apiService.post(`/ai-teacher/recommendations/${studentId}/generate/`);
  return normalizeResponse(res);
  }

  // Behavioral Analysis
  static async analyzeBehavior(studentId: number, data: any): Promise<any> {
  const res = await apiService.post(`/ai-teacher/behavior-analysis/${studentId}/`, data);
  return normalizeResponse(res);
  }

  static async getBehaviorReport(studentId: number, dateRange?: string): Promise<any> {
    const params = dateRange ? { date_range: dateRange } : {};
  const res = await apiService.get(`/ai-teacher/behavior-analysis/${studentId}/report/`, { params });
  return normalizeResponse(res);
  }

  // AI Model Management
  static async getAIModels(): Promise<any[]> {
  const res = await apiService.get('/ai-teacher/models/');
  return normalizeResponse(res);
  }

  static async getAIModel(id: string): Promise<any> {
  const res = await apiService.get(`/ai-teacher/models/${id}/`);
  return normalizeResponse(res);
  }

  static async trainAIModel(modelId: string, data: any): Promise<any> {
  const res = await apiService.post(`/ai-teacher/models/${modelId}/train/`, data);
  return normalizeResponse(res);
  }

  static async deployAIModel(modelId: string): Promise<any> {
  const res = await apiService.post(`/ai-teacher/models/${modelId}/deploy/`);
  return normalizeResponse(res);
  }

  // AI Insights
  static async getAIInsights(studentId: number): Promise<any> {
  const res = await apiService.get(`/ai-teacher/insights/${studentId}/`);
  return normalizeResponse(res);
  }

  static async generateAIInsights(studentId: number): Promise<any> {
  const res = await apiService.post(`/ai-teacher/insights/${studentId}/generate/`);
  return normalizeResponse(res);
  }
}

export default AITeacherApiService;