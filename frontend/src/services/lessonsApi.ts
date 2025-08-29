import { apiService } from './api';
import { 
  Lesson, 
  LessonMaterial, 
  LessonAssessment,
  PaginatedResponse 
} from '../types';

// Lessons API Service
export class LessonsApiService {
  // Lessons
  static async getLessons(params?: {
    page?: number;
    page_size?: number;
    subject?: string;
    grade_level?: number;
    teacher_id?: number;
  }): Promise<PaginatedResponse<Lesson>> {
    return apiService.get('/lessons/', { params });
  }

  static async getLesson(id: number): Promise<Lesson> {
    return apiService.get(`/lessons/${id}/`);
  }

  static async createLesson(data: Partial<Lesson>): Promise<Lesson> {
    return apiService.post('/lessons/', data);
  }

  static async updateLesson(id: number, data: Partial<Lesson>): Promise<Lesson> {
    return apiService.put(`/lessons/${id}/`, data);
  }

  static async deleteLesson(id: number): Promise<void> {
    return apiService.delete(`/lessons/${id}/`);
  }

  // Lesson Plans
  static async getLessonPlans(lessonId: number): Promise<any[]> {
    return apiService.get(`/lessons/${lessonId}/plans/`);
  }

  static async getLessonPlan(lessonId: number, planId: number): Promise<any> {
    return apiService.get(`/lessons/${lessonId}/plans/${planId}/`);
  }

  static async createLessonPlan(lessonId: number, data: any): Promise<any> {
    return apiService.post(`/lessons/${lessonId}/plans/`, data);
  }

  static async updateLessonPlan(lessonId: number, planId: number, data: any): Promise<any> {
    return apiService.put(`/lessons/${lessonId}/plans/${planId}/`, data);
  }

  static async deleteLessonPlan(lessonId: number, planId: number): Promise<void> {
    return apiService.delete(`/lessons/${lessonId}/plans/${planId}/`);
  }

  // Lesson Materials
  static async getLessonMaterials(lessonId: number): Promise<LessonMaterial[]> {
    return apiService.get(`/lessons/${lessonId}/materials/`);
  }

  static async getLessonMaterial(lessonId: number, materialId: number): Promise<LessonMaterial> {
    return apiService.get(`/lessons/${lessonId}/materials/${materialId}/`);
  }

  static async createLessonMaterial(lessonId: number, data: Partial<LessonMaterial>): Promise<LessonMaterial> {
    return apiService.post(`/lessons/${lessonId}/materials/`, data);
  }

  static async updateLessonMaterial(lessonId: number, materialId: number, data: Partial<LessonMaterial>): Promise<LessonMaterial> {
    return apiService.put(`/lessons/${lessonId}/materials/${materialId}/`, data);
  }

  static async deleteLessonMaterial(lessonId: number, materialId: number): Promise<void> {
    return apiService.delete(`/lessons/${lessonId}/materials/${materialId}/`);
  }

  // Lesson Assessments
  static async getLessonAssessments(lessonId: number): Promise<LessonAssessment[]> {
    return apiService.get(`/lessons/${lessonId}/assessments/`);
  }

  static async getLessonAssessment(lessonId: number, assessmentId: number): Promise<LessonAssessment> {
    return apiService.get(`/lessons/${lessonId}/assessments/${assessmentId}/`);
  }

  static async createLessonAssessment(lessonId: number, data: Partial<LessonAssessment>): Promise<LessonAssessment> {
    return apiService.post(`/lessons/${lessonId}/assessments/`, data);
  }

  static async updateLessonAssessment(lessonId: number, assessmentId: number, data: Partial<LessonAssessment>): Promise<LessonAssessment> {
    return apiService.put(`/lessons/${lessonId}/assessments/${assessmentId}/`, data);
  }

  static async deleteLessonAssessment(lessonId: number, assessmentId: number): Promise<void> {
    return apiService.delete(`/lessons/${lessonId}/assessments/${assessmentId}/`);
  }

  // Search Lessons
  static async searchLessons(query: string): Promise<PaginatedResponse<Lesson>> {
    return apiService.get('/lessons/search/', { params: { q: query } });
  }
}

export default LessonsApiService;