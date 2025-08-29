import { apiService } from './api';
import { 
  LearningAnalytics, 
  PerformanceMetrics, 
  PaginatedResponse 
} from '../types';

// Analytics API Service
export class AnalyticsApiService {
  // Learning Analytics
  static async getLearningAnalytics(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    subject?: string;
    time_period?: string;
  }): Promise<PaginatedResponse<LearningAnalytics>> {
    return apiService.get('/analytics/learning-analytics/', { params });
  }

  static async getLearningAnalyticsById(id: number): Promise<LearningAnalytics> {
    return apiService.get(`/analytics/learning-analytics/${id}/`);
  }

  static async createLearningAnalytics(data: Partial<LearningAnalytics>): Promise<LearningAnalytics> {
    return apiService.post('/analytics/learning-analytics/', data);
  }

  static async updateLearningAnalytics(id: number, data: Partial<LearningAnalytics>): Promise<LearningAnalytics> {
    return apiService.put(`/analytics/learning-analytics/${id}/`, data);
  }

  static async deleteLearningAnalytics(id: number): Promise<void> {
    return apiService.delete(`/analytics/learning-analytics/${id}/`);
  }

  // Performance Metrics
  static async getPerformanceMetrics(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    subject?: string;
    assessment_type?: string;
  }): Promise<PaginatedResponse<PerformanceMetrics>> {
    return apiService.get('/analytics/performance-metrics/', { params });
  }

  static async getPerformanceMetricsById(id: number): Promise<PerformanceMetrics> {
    return apiService.get(`/analytics/performance-metrics/${id}/`);
  }

  static async createPerformanceMetrics(data: Partial<PerformanceMetrics>): Promise<PerformanceMetrics> {
    return apiService.post('/analytics/performance-metrics/', data);
  }

  static async updatePerformanceMetrics(id: number, data: Partial<PerformanceMetrics>): Promise<PerformanceMetrics> {
    return apiService.put(`/analytics/performance-metrics/${id}/`, data);
  }

  static async deletePerformanceMetrics(id: number): Promise<void> {
    return apiService.delete(`/analytics/performance-metrics/${id}/`);
  }

  // Engagement Analytics
  static async getEngagementAnalytics(studentId?: number): Promise<any[]> {
    const params = studentId ? { student_id: studentId } : {};
    return apiService.get('/analytics/engagement-analytics/', { params });
  }

  static async getEngagementAnalyticsById(id: number): Promise<any> {
    return apiService.get(`/analytics/engagement-analytics/${id}/`);
  }

  // Dashboard Configuration
  static async getDashboardConfigurations(): Promise<any[]> {
    return apiService.get('/analytics/dashboard-configurations/');
  }

  static async getDashboardConfiguration(id: number): Promise<any> {
    return apiService.get(`/analytics/dashboard-configurations/${id}/`);
  }

  static async createDashboardConfiguration(data: any): Promise<any> {
    return apiService.post('/analytics/dashboard-configurations/', data);
  }

  static async updateDashboardConfiguration(id: number, data: any): Promise<any> {
    return apiService.put(`/analytics/dashboard-configurations/${id}/`, data);
  }

  static async deleteDashboardConfiguration(id: number): Promise<void> {
    return apiService.delete(`/analytics/dashboard-configurations/${id}/`);
  }

  // Report Templates
  static async getReportTemplates(): Promise<any[]> {
    return apiService.get('/analytics/report-templates/');
  }

  static async getReportTemplate(id: number): Promise<any> {
    return apiService.get(`/analytics/report-templates/${id}/`);
  }

  static async createReportTemplate(data: any): Promise<any> {
    return apiService.post('/analytics/report-templates/', data);
  }

  static async updateReportTemplate(id: number, data: any): Promise<any> {
    return apiService.put(`/analytics/report-templates/${id}/`, data);
  }

  static async deleteReportTemplate(id: number): Promise<void> {
    return apiService.delete(`/analytics/report-templates/${id}/`);
  }

  // Student Analytics Dashboard
  static async getStudentAnalyticsDashboard(studentId: number): Promise<any> {
    return apiService.get(`/analytics/student-dashboard/${studentId}/`);
  }

  // Class Analytics Dashboard
  static async getClassAnalyticsDashboard(classId: number): Promise<any> {
    return apiService.get(`/analytics/class-dashboard/${classId}/`);
  }

  // Generate Reports
  static async generateReport(reportType: string, params: any): Promise<any> {
    return apiService.post('/analytics/generate-report/', {
      report_type: reportType,
      ...params
    });
  }

  // Export Data
  static async exportData(format: string, params: any): Promise<any> {
    return apiService.get('/analytics/export/', {
      params: { format, ...params }
    });
  }

  // AI-Generated Insights
  static async getAIInsights(studentId?: number): Promise<any[]> {
    const params = studentId ? { student_id: studentId } : {};
    return apiService.get('/analytics/ai-insights/', { params });
  }

  static async generateAIInsights(studentId: number): Promise<any> {
    return apiService.post(`/analytics/ai-insights/${studentId}/generate/`);
  }

  // Predictive Analytics
  static async getPredictions(studentId: number): Promise<any> {
    return apiService.get(`/analytics/predictions/${studentId}/`);
  }

  static async generatePredictions(studentId: number): Promise<any> {
    return apiService.post(`/analytics/predictions/${studentId}/generate/`);
  }

  // Risk Assessment
  static async getRiskAssessment(studentId: number): Promise<any> {
    return apiService.get(`/analytics/risk-assessment/${studentId}/`);
  }

  static async generateRiskAssessment(studentId: number): Promise<any> {
    return apiService.post(`/analytics/risk-assessment/${studentId}/generate/`);
  }

  // Trend Analysis
  static async getTrendAnalysis(params: {
    student_id?: number;
    subject?: string;
    time_period?: string;
    metric?: string;
  }): Promise<any> {
    return apiService.get('/analytics/trend-analysis/', { params });
  }

  // Comparative Analysis
  static async getComparativeAnalysis(params: {
    student_ids: number[];
    subjects?: string[];
    time_period?: string;
  }): Promise<any> {
    return apiService.post('/analytics/comparative-analysis/', params);
  }
}

export default AnalyticsApiService;