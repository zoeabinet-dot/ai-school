import { apiService } from './api';
import { 
  WebcamSession, 
  BehaviorEvent, 
  PrivacySettings,
  PaginatedResponse 
} from '../types';

// Monitoring API Service
export class MonitoringApiService {
  // Webcam Sessions
  static async getWebcamSessions(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    status?: string;
  }): Promise<PaginatedResponse<WebcamSession>> {
    return apiService.get('/monitoring/webcam-sessions/', { params });
  }

  static async getWebcamSession(id: number): Promise<WebcamSession> {
    return apiService.get(`/monitoring/webcam-sessions/${id}/`);
  }

  static async createWebcamSession(data: Partial<WebcamSession>): Promise<WebcamSession> {
    return apiService.post('/monitoring/webcam-sessions/', data);
  }

  static async updateWebcamSession(id: number, data: Partial<WebcamSession>): Promise<WebcamSession> {
    return apiService.put(`/monitoring/webcam-sessions/${id}/`, data);
  }

  static async deleteWebcamSession(id: number): Promise<void> {
    return apiService.delete(`/monitoring/webcam-sessions/${id}/`);
  }

  // Frame Analysis
  static async getFrameAnalysis(sessionId: number): Promise<any[]> {
    return apiService.get(`/monitoring/webcam-sessions/${sessionId}/frame-analysis/`);
  }

  static async analyzeFrame(sessionId: number, frameData: any): Promise<any> {
    return apiService.post(`/monitoring/webcam-sessions/${sessionId}/analyze-frame/`, frameData);
  }

  // Behavior Events
  static async getBehaviorEvents(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    event_type?: string;
    severity?: string;
  }): Promise<PaginatedResponse<BehaviorEvent>> {
    return apiService.get('/monitoring/behavior-events/', { params });
  }

  static async getBehaviorEvent(id: number): Promise<BehaviorEvent> {
    return apiService.get(`/monitoring/behavior-events/${id}/`);
  }

  static async createBehaviorEvent(data: Partial<BehaviorEvent>): Promise<BehaviorEvent> {
    return apiService.post('/monitoring/behavior-events/', data);
  }

  static async updateBehaviorEvent(id: number, data: Partial<BehaviorEvent>): Promise<BehaviorEvent> {
    return apiService.put(`/monitoring/behavior-events/${id}/`, data);
  }

  static async deleteBehaviorEvent(id: number): Promise<void> {
    return apiService.delete(`/monitoring/behavior-events/${id}/`);
  }

  // Privacy Settings
  static async getPrivacySettings(studentId: number): Promise<PrivacySettings> {
    return apiService.get(`/monitoring/privacy-settings/${studentId}/`);
  }

  static async updatePrivacySettings(studentId: number, data: Partial<PrivacySettings>): Promise<PrivacySettings> {
    return apiService.put(`/monitoring/privacy-settings/${studentId}/`, data);
  }

  // Monitoring Alerts
  static async getMonitoringAlerts(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    severity?: string;
    resolved?: boolean;
  }): Promise<any[]> {
    return apiService.get('/monitoring/alerts/', { params });
  }

  static async getMonitoringAlert(id: number): Promise<any> {
    return apiService.get(`/monitoring/alerts/${id}/`);
  }

  static async createMonitoringAlert(data: any): Promise<any> {
    return apiService.post('/monitoring/alerts/', data);
  }

  static async updateMonitoringAlert(id: number, data: any): Promise<any> {
    return apiService.put(`/monitoring/alerts/${id}/`, data);
  }

  static async deleteMonitoringAlert(id: number): Promise<void> {
    return apiService.delete(`/monitoring/alerts/${id}/`);
  }

  static async resolveAlert(id: number): Promise<any> {
    return apiService.post(`/monitoring/alerts/${id}/resolve/`);
  }

  // Student Monitoring Dashboard
  static async getStudentMonitoringDashboard(studentId: number): Promise<any> {
    return apiService.get(`/monitoring/student-dashboard/${studentId}/`);
  }

  // Real-time Monitoring
  static async startRealTimeMonitoring(studentId: number, settings: any): Promise<any> {
    return apiService.post(`/monitoring/real-time/${studentId}/start/`, settings);
  }

  static async stopRealTimeMonitoring(sessionId: number): Promise<void> {
    return apiService.post(`/monitoring/real-time/${sessionId}/stop/`);
  }

  static async getRealTimeStatus(sessionId: number): Promise<any> {
    return apiService.get(`/monitoring/real-time/${sessionId}/status/`);
  }

  // AI Behavior Analysis
  static async analyzeBehaviorAI(studentId: number, data: any): Promise<any> {
    return apiService.post(`/monitoring/ai-behavior-analysis/${studentId}/`, data);
  }

  static async getBehaviorReport(studentId: number, dateRange?: string): Promise<any> {
    const params = dateRange ? { date_range: dateRange } : {};
    return apiService.get(`/monitoring/behavior-report/${studentId}/`, { params });
  }

  // Privacy Compliance
  static async checkPrivacyCompliance(studentId: number): Promise<any> {
    return apiService.get(`/monitoring/privacy-compliance/${studentId}/`);
  }

  static async generatePrivacyReport(studentId: number): Promise<any> {
    return apiService.post(`/monitoring/privacy-compliance/${studentId}/report/`);
  }

  // Data Export
  static async exportMonitoringData(studentId: number, format: string, dateRange?: string): Promise<any> {
    const params = { format, ...(dateRange && { date_range: dateRange }) };
    return apiService.get(`/monitoring/export/${studentId}/`, { params });
  }
}

export default MonitoringApiService;