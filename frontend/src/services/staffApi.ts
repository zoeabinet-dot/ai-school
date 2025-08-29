import { apiService } from './api';
import { 
  Staff, 
  StaffAssignment,
  PaginatedResponse 
} from '../types';

// Staff API Service
export class StaffApiService {
  // Staff Members
  static async getStaffMembers(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    department?: string;
    role?: string;
  }): Promise<PaginatedResponse<Staff>> {
    return apiService.get('/staff/', { params });
  }

  static async getStaffMember(id: number): Promise<Staff> {
    return apiService.get(`/staff/${id}/`);
  }

  static async createStaffMember(data: Partial<Staff>): Promise<Staff> {
    return apiService.post('/staff/', data);
  }

  static async updateStaffMember(id: number, data: Partial<Staff>): Promise<Staff> {
    return apiService.put(`/staff/${id}/`, data);
  }

  static async deleteStaffMember(id: number): Promise<void> {
    return apiService.delete(`/staff/${id}/`);
  }

  // Staff Assignments
  static async getStaffAssignments(staffId: number): Promise<StaffAssignment[]> {
    return apiService.get(`/staff/${staffId}/assignments/`);
  }

  static async getStaffAssignment(staffId: number, assignmentId: number): Promise<StaffAssignment> {
    return apiService.get(`/staff/${staffId}/assignments/${assignmentId}/`);
  }

  static async createStaffAssignment(staffId: number, data: Partial<StaffAssignment>): Promise<StaffAssignment> {
    return apiService.post(`/staff/${staffId}/assignments/`, data);
  }

  static async updateStaffAssignment(staffId: number, assignmentId: number, data: Partial<StaffAssignment>): Promise<StaffAssignment> {
    return apiService.put(`/staff/${staffId}/assignments/${assignmentId}/`, data);
  }

  static async deleteStaffAssignment(staffId: number, assignmentId: number): Promise<void> {
    return apiService.delete(`/staff/${staffId}/assignments/${assignmentId}/`);
  }

  // Staff Dashboard
  static async getStaffDashboard(staffId: number): Promise<any> {
    return apiService.get(`/staff/${staffId}/dashboard/`);
  }

  // Search Staff
  static async searchStaff(query: string): Promise<PaginatedResponse<Staff>> {
    return apiService.get('/staff/search/', { params: { q: query } });
  }
}

export default StaffApiService;