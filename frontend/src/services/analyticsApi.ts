import { apiService } from './api';
import { 
  LearningAnalytics, 
  PerformanceMetrics, 
  PaginatedResponse 
} from '../types';

// Analytics API Service
export class AnalyticsApiService {
  static normalizeResponse(res: any) {
    if (res && typeof res === 'object') {
      if (res.data && Object.prototype.hasOwnProperty.call(res.data, 'results')) return res;
      if (res.data) return res.data;
    }
    return res;
  }
  // Learning Analytics
  static async getLearningAnalytics(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    subject?: string;
    time_period?: string;
  }): Promise<PaginatedResponse<LearningAnalytics>> {
  const res = await apiService.get('/analytics/learning-analytics/', { params });
  return AnalyticsApiService.normalizeResponse(res);
  }

  static async getLearningAnalyticsById(id: number): Promise<LearningAnalytics> {
  const res = await apiService.get(`/analytics/learning-analytics/${id}/`);
  return AnalyticsApiService.normalizeResponse(res);
  }

  static async createLearningAnalytics(data: Partial<LearningAnalytics>): Promise<LearningAnalytics> {
  const res = await apiService.post('/analytics/learning-analytics/', data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateLearningAnalytics(id: number, data: any): Promise<LearningAnalytics> {
  const res = await apiService.put(`/analytics/learning-analytics/${id}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteLearningAnalytics(id: number): Promise<void> {
  const res = await apiService.delete(`/analytics/learning-analytics/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Performance Metrics
  static async getPerformanceMetrics(params?: {
    page?: number;
    page_size?: number;
    student_id?: number;
    subject?: string;
    assessment_type?: string;
  }): Promise<PaginatedResponse<PerformanceMetrics>> {
  const res = await apiService.get('/analytics/performance-metrics/', { params });
  return (res && typeof res === 'object' && 'results' in res) ? res : res;
  }

  static async getPerformanceMetricsById(id: number): Promise<PerformanceMetrics> {
  const res = await apiService.get(`/analytics/performance-metrics/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createPerformanceMetrics(data: Partial<PerformanceMetrics>): Promise<PerformanceMetrics> {
  const res = await apiService.post('/analytics/performance-metrics/', data);
  return AnalyticsApiService.normalizeResponse(res);
  }

  static async updatePerformanceMetrics(id: number, data: Partial<PerformanceMetrics>): Promise<PerformanceMetrics> {
  const res = await apiService.put(`/analytics/performance-metrics/${id}/`, data);
  return AnalyticsApiService.normalizeResponse(res);
  }

  static async deletePerformanceMetrics(id: number): Promise<void> {
  const res = await apiService.delete(`/analytics/performance-metrics/${id}/`);
  return AnalyticsApiService.normalizeResponse(res);
  }

  // Engagement Analytics
  static async getEngagementAnalytics(studentId?: number): Promise<any[]> {
    const params = studentId ? { student_id: studentId } : {};
  const res = await apiService.get('/analytics/engagement-analytics/', { params });
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async getEngagementAnalyticsById(id: number): Promise<any> {
  const res = await apiService.get(`/analytics/engagement-analytics/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Dashboard Configuration
  static async getDashboardConfigurations(): Promise<any[]> {
  const res = await apiService.get('/analytics/dashboard-configurations/');
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async getDashboardConfiguration(id: number): Promise<any> {
  const res = await apiService.get(`/analytics/dashboard-configurations/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createDashboardConfiguration(data: any): Promise<any> {
  const res = await apiService.post('/analytics/dashboard-configurations/', data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateDashboardConfiguration(id: number, data: any): Promise<any> {
  const res = await apiService.put(`/analytics/dashboard-configurations/${id}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteDashboardConfiguration(id: number): Promise<void> {
  const res = await apiService.delete(`/analytics/dashboard-configurations/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Report Templates
  static async getReportTemplates(): Promise<any[]> {
  const res = await apiService.get('/analytics/report-templates/');
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async getReportTemplate(id: number): Promise<any> {
  const res = await apiService.get(`/analytics/report-templates/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async createReportTemplate(data: any): Promise<any> {
  const res = await apiService.post('/analytics/report-templates/', data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async updateReportTemplate(id: number, data: any): Promise<any> {
  const res = await apiService.put(`/analytics/report-templates/${id}/`, data);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async deleteReportTemplate(id: number): Promise<void> {
  const res = await apiService.delete(`/analytics/report-templates/${id}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Student Analytics Dashboard
  static async getStudentAnalyticsDashboard(studentId: number): Promise<any> {
  const res = await apiService.get(`/analytics/student-dashboard/${studentId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Class Analytics Dashboard
  static async getClassAnalyticsDashboard(classId: number): Promise<any> {
  const res = await apiService.get(`/analytics/class-dashboard/${classId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Generate Reports
  static async generateReport(reportType: string, params: any): Promise<any> {
  const res = await apiService.post('/analytics/generate-report/', {
      report_type: reportType,
      ...params
    });
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Export Data
  static async exportData(format: string, params: any): Promise<any> {
    const res = await apiService.get('/analytics/export/', {
      params: { format, ...params }
    });
    return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // AI-Generated Insights
  static async getAIInsights(studentId?: number): Promise<any[]> {
    const params = studentId ? { student_id: studentId } : {};
  const res = await apiService.get('/analytics/ai-insights/', { params });
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async generateAIInsights(studentId: number): Promise<any> {
  const res = await apiService.post(`/analytics/ai-insights/${studentId}/generate/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Predictive Analytics
  static async getPredictions(studentId: number): Promise<any> {
  const res = await apiService.get(`/analytics/predictions/${studentId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async generatePredictions(studentId: number): Promise<any> {
  const res = await apiService.post(`/analytics/predictions/${studentId}/generate/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Risk Assessment
  static async getRiskAssessment(studentId: number): Promise<any> {
  const res = await apiService.get(`/analytics/risk-assessment/${studentId}/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  static async generateRiskAssessment(studentId: number): Promise<any> {
  const res = await apiService.post(`/analytics/risk-assessment/${studentId}/generate/`);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Trend Analysis
  static async getTrendAnalysis(params: {
    student_id?: number;
    subject?: string;
    time_period?: string;
    metric?: string;
  }): Promise<any> {
  const res = await apiService.get('/analytics/trend-analysis/', { params });
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }

  // Comparative Analysis
  static async getComparativeAnalysis(params: {
    student_ids: number[];
    subjects?: string[];
    time_period?: string;
  }): Promise<any> {
  const res = await apiService.post('/analytics/comparative-analysis/', params);
  return (res && typeof res === 'object' && 'data' in res) ? res.data : res;
  }
}

export default AnalyticsApiService;