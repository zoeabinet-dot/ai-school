import { apiService } from './api';

function normalizeResponse(res: any) {
  if (res && typeof res === 'object') {
    if (res.data && Object.prototype.hasOwnProperty.call(res.data, 'results')) return res;
    if (res.data) return res.data;
  }
  return res;
}
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
  const res = await apiService.get('/students/', { params });
  return normalizeResponse(res);
  }

  // Get student by ID
  static async getStudent(id: number): Promise<Student> {
  const res = await apiService.get(`/students/${id}/`);
  // tests expect the full response object for single student fetch
  return res;
  }

  // Create new student
  static async createStudent(data: any): Promise<Student> {
  const res = await apiService.post('/students/', data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Update student
  static async updateStudent(id: number, data: any): Promise<Student> {
  const res = await apiService.put(`/students/${id}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Delete student
  static async deleteStudent(id: number): Promise<void> {
  const res = await apiService.delete(`/students/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Search students
  static async searchStudents(query: string): Promise<PaginatedResponse<Student>> {
  const res = await apiService.get('/students/search/', { params: { q: query } });
  return (res && typeof res === 'object' && 'results' in res) ? res : res;
  }

  // Get student dashboard
  static async getStudentDashboard(id: number): Promise<any> {
  const res = await apiService.get(`/students/${id}/dashboard/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Academic Records
  static async getAcademicRecords(studentId: number): Promise<AcademicRecord[]> {
  const res = await apiService.get(`/students/${studentId}/academic-records/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createAcademicRecord(studentId: number, data: Partial<AcademicRecord>): Promise<AcademicRecord> {
  const res = await apiService.post(`/students/${studentId}/academic-records/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateAcademicRecord(studentId: number, recordId: number, data: Partial<AcademicRecord>): Promise<AcademicRecord> {
  const res = await apiService.put(`/students/${studentId}/academic-records/${recordId}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteAcademicRecord(studentId: number, recordId: number): Promise<void> {
  const res = await apiService.delete(`/students/${studentId}/academic-records/${recordId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Student Projects
  static async getStudentProjects(studentId: number): Promise<StudentProject[]> {
  const res = await apiService.get(`/students/${studentId}/projects/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createStudentProject(studentId: number, data: Partial<StudentProject>): Promise<StudentProject> {
  const res = await apiService.post(`/students/${studentId}/projects/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateStudentProject(studentId: number, projectId: number, data: Partial<StudentProject>): Promise<StudentProject> {
  const res = await apiService.put(`/students/${studentId}/projects/${projectId}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteStudentProject(studentId: number, projectId: number): Promise<void> {
  const res = await apiService.delete(`/students/${studentId}/projects/${projectId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Learning Sessions
  static async getLearningSessions(studentId: number): Promise<LearningSession[]> {
  const res = await apiService.get(`/students/${studentId}/learning-sessions/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createLearningSession(studentId: number, data: Partial<LearningSession>): Promise<LearningSession> {
  const res = await apiService.post(`/students/${studentId}/learning-sessions/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateLearningSession(studentId: number, sessionId: number, data: Partial<LearningSession>): Promise<LearningSession> {
  const res = await apiService.put(`/students/${studentId}/learning-sessions/${sessionId}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteLearningSession(studentId: number, sessionId: number): Promise<void> {
  const res = await apiService.delete(`/students/${studentId}/learning-sessions/${sessionId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Student Goals
  static async getStudentGoals(studentId: number): Promise<StudentGoal[]> {
  const res = await apiService.get(`/students/${studentId}/goals/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createStudentGoal(studentId: number, data: Partial<StudentGoal>): Promise<StudentGoal> {
  const res = await apiService.post(`/students/${studentId}/goals/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateStudentGoal(studentId: number, goalId: number, data: Partial<StudentGoal>): Promise<StudentGoal> {
  const res = await apiService.put(`/students/${studentId}/goals/${goalId}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteStudentGoal(studentId: number, goalId: number): Promise<void> {
  const res = await apiService.delete(`/students/${studentId}/goals/${goalId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }
}

export default StudentsApiService;