import { apiService } from './api';
import { 
  Student, 
  AcademicRecord, 
  StudentProject, 
  LearningSession, 
  StudentGoal,
  PaginatedResponse 
} from '../types';

// Students API Service
export class StudentsApiService {
  // Get all students with pagination
  static async getStudents(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    grade_level?: number;
    academic_status?: string;
  }): Promise<PaginatedResponse<Student>> {
    return apiService.get('/students/', { params });
  }

  // Get student by ID
  static async getStudent(id: number): Promise<Student> {
    return apiService.get(`/students/${id}/`);
  }

  // Create new student
  static async createStudent(data: Partial<Student>): Promise<Student> {
    return apiService.post('/students/', data);
  }

  // Update student
  static async updateStudent(id: number, data: Partial<Student>): Promise<Student> {
    return apiService.put(`/students/${id}/`, data);
  }

  // Delete student
  static async deleteStudent(id: number): Promise<void> {
    return apiService.delete(`/students/${id}/`);
  }

  // Search students
  static async searchStudents(query: string): Promise<PaginatedResponse<Student>> {
    return apiService.get('/students/search/', { params: { q: query } });
  }

  // Get student dashboard
  static async getStudentDashboard(id: number): Promise<any> {
    return apiService.get(`/students/${id}/dashboard/`);
  }

  // Academic Records
  static async getAcademicRecords(studentId: number): Promise<AcademicRecord[]> {
    return apiService.get(`/students/${studentId}/academic-records/`);
  }

  static async createAcademicRecord(studentId: number, data: Partial<AcademicRecord>): Promise<AcademicRecord> {
    return apiService.post(`/students/${studentId}/academic-records/`, data);
  }

  static async updateAcademicRecord(studentId: number, recordId: number, data: Partial<AcademicRecord>): Promise<AcademicRecord> {
    return apiService.put(`/students/${studentId}/academic-records/${recordId}/`, data);
  }

  static async deleteAcademicRecord(studentId: number, recordId: number): Promise<void> {
    return apiService.delete(`/students/${studentId}/academic-records/${recordId}/`);
  }

  // Student Projects
  static async getStudentProjects(studentId: number): Promise<StudentProject[]> {
    return apiService.get(`/students/${studentId}/projects/`);
  }

  static async createStudentProject(studentId: number, data: Partial<StudentProject>): Promise<StudentProject> {
    return apiService.post(`/students/${studentId}/projects/`, data);
  }

  static async updateStudentProject(studentId: number, projectId: number, data: Partial<StudentProject>): Promise<StudentProject> {
    return apiService.put(`/students/${studentId}/projects/${projectId}/`, data);
  }

  static async deleteStudentProject(studentId: number, projectId: number): Promise<void> {
    return apiService.delete(`/students/${studentId}/projects/${projectId}/`);
  }

  // Learning Sessions
  static async getLearningSessions(studentId: number): Promise<LearningSession[]> {
    return apiService.get(`/students/${studentId}/learning-sessions/`);
  }

  static async createLearningSession(studentId: number, data: Partial<LearningSession>): Promise<LearningSession> {
    return apiService.post(`/students/${studentId}/learning-sessions/`, data);
  }

  static async updateLearningSession(studentId: number, sessionId: number, data: Partial<LearningSession>): Promise<LearningSession> {
    return apiService.put(`/students/${studentId}/learning-sessions/${sessionId}/`, data);
  }

  static async deleteLearningSession(studentId: number, sessionId: number): Promise<void> {
    return apiService.delete(`/students/${studentId}/learning-sessions/${sessionId}/`);
  }

  // Student Goals
  static async getStudentGoals(studentId: number): Promise<StudentGoal[]> {
    return apiService.get(`/students/${studentId}/goals/`);
  }

  static async createStudentGoal(studentId: number, data: Partial<StudentGoal>): Promise<StudentGoal> {
    return apiService.post(`/students/${studentId}/goals/`, data);
  }

  static async updateStudentGoal(studentId: number, goalId: number, data: Partial<StudentGoal>): Promise<StudentGoal> {
    return apiService.put(`/students/${studentId}/goals/${goalId}/`, data);
  }

  static async deleteStudentGoal(studentId: number, goalId: number): Promise<void> {
    return apiService.delete(`/students/${studentId}/goals/${goalId}/`);
  }
}

export default StudentsApiService;