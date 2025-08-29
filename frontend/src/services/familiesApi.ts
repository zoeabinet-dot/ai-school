import { apiService } from './api';
import { 
  Family, 
  FamilyMember, 
  FamilyStudent,
  PaginatedResponse 
} from '../types';

// Families API Service
export class FamiliesApiService {
  // Families
  static async getFamilies(params?: {
    page?: number;
    page_size?: number;
    search?: string;
  }): Promise<PaginatedResponse<Family>> {
    return apiService.get('/families/', { params });
  }

  static async getFamily(id: number): Promise<Family> {
    return apiService.get(`/families/${id}/`);
  }

  static async createFamily(data: Partial<Family>): Promise<Family> {
    return apiService.post('/families/', data);
  }

  static async updateFamily(id: number, data: Partial<Family>): Promise<Family> {
    return apiService.put(`/families/${id}/`, data);
  }

  static async deleteFamily(id: number): Promise<void> {
    return apiService.delete(`/families/${id}/`);
  }

  // Family Members
  static async getFamilyMembers(familyId: number): Promise<FamilyMember[]> {
    return apiService.get(`/families/${familyId}/members/`);
  }

  static async getFamilyMember(familyId: number, memberId: number): Promise<FamilyMember> {
    return apiService.get(`/families/${familyId}/members/${memberId}/`);
  }

  static async createFamilyMember(familyId: number, data: Partial<FamilyMember>): Promise<FamilyMember> {
    return apiService.post(`/families/${familyId}/members/`, data);
  }

  static async updateFamilyMember(familyId: number, memberId: number, data: Partial<FamilyMember>): Promise<FamilyMember> {
    return apiService.put(`/families/${familyId}/members/${memberId}/`, data);
  }

  static async deleteFamilyMember(familyId: number, memberId: number): Promise<void> {
    return apiService.delete(`/families/${familyId}/members/${memberId}/`);
  }

  // Family Students
  static async getFamilyStudents(familyId: number): Promise<FamilyStudent[]> {
    return apiService.get(`/families/${familyId}/students/`);
  }

  static async getFamilyStudent(familyId: number, studentId: number): Promise<FamilyStudent> {
    return apiService.get(`/families/${familyId}/students/${studentId}/`);
  }

  static async createFamilyStudent(familyId: number, data: Partial<FamilyStudent>): Promise<FamilyStudent> {
    return apiService.post(`/families/${familyId}/students/`, data);
  }

  static async updateFamilyStudent(familyId: number, studentId: number, data: Partial<FamilyStudent>): Promise<FamilyStudent> {
    return apiService.put(`/families/${familyId}/students/${studentId}/`, data);
  }

  static async deleteFamilyStudent(familyId: number, studentId: number): Promise<void> {
    return apiService.delete(`/families/${familyId}/students/${studentId}/`);
  }

  // Family Dashboard
  static async getFamilyDashboard(familyId: number): Promise<any> {
    return apiService.get(`/families/${familyId}/dashboard/`);
  }

  // Search Families
  static async searchFamilies(query: string): Promise<PaginatedResponse<Family>> {
    return apiService.get('/families/search/', { params: { q: query } });
  }
}

export default FamiliesApiService;