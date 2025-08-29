import { apiService } from '../api';
import AnalyticsApiService from '../analyticsApi';
import { mockLearningAnalytics, mockPaginatedResponse } from '../../utils/testUtils';

// Mock the API service
jest.mock('../api', () => ({
  apiService: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

describe('AnalyticsApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getLearningAnalytics', () => {
    it('should fetch learning analytics with default parameters', async () => {
      const mockResponse = mockPaginatedResponse([mockLearningAnalytics]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getLearningAnalytics();

      expect(apiService.get).toHaveBeenCalledWith('/analytics/learning-analytics/', { params: undefined });
      expect(result).toEqual(mockResponse);
    });

    it('should fetch learning analytics with custom parameters', async () => {
      const params = {
        page: 1,
        page_size: 10,
        student_id: 1,
        subject: 'Mathematics',
        time_period: 'weekly',
      };
      const mockResponse = mockPaginatedResponse([mockLearningAnalytics]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getLearningAnalytics(params);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/learning-analytics/', { params });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getLearningAnalyticsById', () => {
    it('should fetch a single learning analytics record by ID', async () => {
      const mockResponse = { data: mockLearningAnalytics };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getLearningAnalyticsById(1);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/learning-analytics/1/');
      expect(result).toEqual(mockLearningAnalytics);
    });
  });

  describe('createLearningAnalytics', () => {
    it('should create a new learning analytics record', async () => {
      const analyticsData = {
        student: 1,
        subject: 'Physics',
        timeSpent: 90,
        completionRate: 0.92,
        engagementScore: 0.85,
        performanceScore: 0.88,
      };
      const mockResponse = { data: mockLearningAnalytics };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.createLearningAnalytics(analyticsData);

      expect(apiService.post).toHaveBeenCalledWith('/analytics/learning-analytics/', analyticsData);
      expect(result).toEqual(mockLearningAnalytics);
    });
  });

  describe('updateLearningAnalytics', () => {
    it('should update an existing learning analytics record', async () => {
      const analyticsData = {
        timeSpent: 120,
        completionRate: 0.95,
      };
      const mockResponse = { data: mockLearningAnalytics };
      (apiService.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.updateLearningAnalytics(1, analyticsData);

      expect(apiService.put).toHaveBeenCalledWith('/analytics/learning-analytics/1/', analyticsData);
      expect(result).toEqual(mockLearningAnalytics);
    });
  });

  describe('deleteLearningAnalytics', () => {
    it('should delete a learning analytics record', async () => {
      (apiService.delete as jest.Mock).mockResolvedValue({});

      await AnalyticsApiService.deleteLearningAnalytics(1);

      expect(apiService.delete).toHaveBeenCalledWith('/analytics/learning-analytics/1/');
    });
  });

  describe('Performance Metrics', () => {
    describe('getPerformanceMetrics', () => {
      it('should fetch performance metrics with parameters', async () => {
        const params = {
          page: 1,
          page_size: 10,
          student_id: 1,
          subject: 'Mathematics',
          assessment_type: 'quiz',
        };
        const performanceMetrics = [
          {
            id: 1,
            student: 1,
            subject: 'Mathematics',
            assessmentType: 'quiz',
            score: 85,
            maxScore: 100,
            date: '2023-12-01',
          },
        ];
        const mockResponse = mockPaginatedResponse(performanceMetrics);
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getPerformanceMetrics(params);

        expect(apiService.get).toHaveBeenCalledWith('/analytics/performance-metrics/', { params });
        expect(result).toEqual(mockResponse);
      });
    });

    describe('createPerformanceMetrics', () => {
      it('should create a new performance metrics record', async () => {
        const metricsData = {
          student: 1,
          subject: 'Physics',
          assessmentType: 'exam',
          score: 92,
          maxScore: 100,
        };
        const mockResponse = { data: metricsData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.createPerformanceMetrics(metricsData);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/performance-metrics/', metricsData);
        expect(result).toEqual(metricsData);
      });
    });
  });

  describe('Engagement Analytics', () => {
    describe('getEngagementAnalytics', () => {
      it('should fetch engagement analytics for all students', async () => {
        const engagementData = [
          {
            id: 1,
            student: 1,
            sessionDuration: 45,
            interactions: 25,
            engagementLevel: 'high',
            date: '2023-12-01',
          },
        ];
        const mockResponse = { data: engagementData };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getEngagementAnalytics();

        expect(apiService.get).toHaveBeenCalledWith('/analytics/engagement-analytics/', { params: {} });
        expect(result).toEqual(engagementData);
      });

      it('should fetch engagement analytics for a specific student', async () => {
        const engagementData = [
          {
            id: 1,
            student: 1,
            sessionDuration: 45,
            interactions: 25,
            engagementLevel: 'high',
            date: '2023-12-01',
          },
        ];
        const mockResponse = { data: engagementData };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getEngagementAnalytics(1);

        expect(apiService.get).toHaveBeenCalledWith('/analytics/engagement-analytics/', { params: { student_id: 1 } });
        expect(result).toEqual(engagementData);
      });
    });
  });

  describe('Dashboard Configuration', () => {
    describe('getDashboardConfigurations', () => {
      it('should fetch all dashboard configurations', async () => {
        const configurations = [
          {
            id: 1,
            name: 'Student Dashboard',
            layout: 'grid',
            widgets: ['performance', 'engagement', 'goals'],
          },
        ];
        const mockResponse = { data: configurations };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getDashboardConfigurations();

        expect(apiService.get).toHaveBeenCalledWith('/analytics/dashboard-configurations/');
        expect(result).toEqual(configurations);
      });
    });

    describe('createDashboardConfiguration', () => {
      it('should create a new dashboard configuration', async () => {
        const configData = {
          name: 'Custom Dashboard',
          layout: 'flexible',
          widgets: ['analytics', 'predictions'],
        };
        const mockResponse = { data: configData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.createDashboardConfiguration(configData);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/dashboard-configurations/', configData);
        expect(result).toEqual(configData);
      });
    });
  });

  describe('Report Templates', () => {
    describe('getReportTemplates', () => {
      it('should fetch all report templates', async () => {
        const templates = [
          {
            id: 1,
            name: 'Student Progress Report',
            type: 'progress',
            format: 'pdf',
            sections: ['performance', 'engagement', 'goals'],
          },
        ];
        const mockResponse = { data: templates };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getReportTemplates();

        expect(apiService.get).toHaveBeenCalledWith('/analytics/report-templates/');
        expect(result).toEqual(templates);
      });
    });

    describe('createReportTemplate', () => {
      it('should create a new report template', async () => {
        const templateData = {
          name: 'Custom Report',
          type: 'comprehensive',
          format: 'excel',
          sections: ['analytics', 'predictions', 'recommendations'],
        };
        const mockResponse = { data: templateData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.createReportTemplate(templateData);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/report-templates/', templateData);
        expect(result).toEqual(templateData);
      });
    });
  });

  describe('Student Analytics Dashboard', () => {
    it('should fetch student analytics dashboard', async () => {
      const dashboardData = {
        student: 1,
        performance: {
          overall: 0.85,
          subjects: {
            mathematics: 0.88,
            physics: 0.82,
          },
        },
        engagement: {
          averageSessionDuration: 45,
          totalSessions: 25,
          engagementLevel: 'high',
        },
        goals: [
          {
            id: 1,
            title: 'Improve Math Skills',
            progress: 0.75,
            target: 0.90,
          },
        ],
      };
      const mockResponse = { data: dashboardData };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getStudentAnalyticsDashboard(1);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/student-dashboard/1/');
      expect(result).toEqual(dashboardData);
    });
  });

  describe('Class Analytics Dashboard', () => {
    it('should fetch class analytics dashboard', async () => {
      const dashboardData = {
        class: 1,
        averagePerformance: 0.82,
        topPerformers: [1, 2, 3],
        subjects: {
          mathematics: { average: 0.85, topStudent: 1 },
          physics: { average: 0.78, topStudent: 2 },
        },
        engagement: {
          averageSessionDuration: 42,
          totalSessions: 150,
        },
      };
      const mockResponse = { data: dashboardData };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getClassAnalyticsDashboard(1);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/class-dashboard/1/');
      expect(result).toEqual(dashboardData);
    });
  });

  describe('Generate Reports', () => {
    it('should generate a report', async () => {
      const reportParams = {
        report_type: 'student_progress',
        student_id: 1,
        time_period: 'monthly',
        format: 'pdf',
      };
      const reportData = {
        id: 1,
        type: 'student_progress',
        url: 'https://example.com/report.pdf',
        generatedAt: '2023-12-01T00:00:00Z',
      };
      const mockResponse = { data: reportData };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.generateReport('student_progress', reportParams);

      expect(apiService.post).toHaveBeenCalledWith('/analytics/generate-report/', {
        report_type: 'student_progress',
        ...reportParams,
      });
      expect(result).toEqual(reportData);
    });
  });

  describe('Export Data', () => {
    it('should export analytics data', async () => {
      const exportParams = {
        format: 'csv',
        student_id: 1,
        time_period: 'weekly',
      };
      const exportData = {
        url: 'https://example.com/export.csv',
        expiresAt: '2023-12-08T00:00:00Z',
      };
      const mockResponse = { data: exportData };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.exportData('csv', exportParams);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/export/', { params: { format: 'csv', ...exportParams } });
      expect(result).toEqual(exportData);
    });
  });

  describe('AI-Generated Insights', () => {
    describe('getAIInsights', () => {
      it('should fetch AI insights for all students', async () => {
        const insights = [
          {
            id: 1,
            type: 'learning_pattern',
            title: 'Optimal Learning Time',
            description: 'Students perform best in morning sessions',
            confidence: 0.88,
          },
        ];
        const mockResponse = { data: insights };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getAIInsights();

        expect(apiService.get).toHaveBeenCalledWith('/analytics/ai-insights/', { params: {} });
        expect(result).toEqual(insights);
      });

      it('should fetch AI insights for a specific student', async () => {
        const insights = [
          {
            id: 1,
            type: 'performance_prediction',
            title: 'Grade Prediction',
            description: 'Expected grade: A-',
            confidence: 0.85,
          },
        ];
        const mockResponse = { data: insights };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getAIInsights(1);

        expect(apiService.get).toHaveBeenCalledWith('/analytics/ai-insights/', { params: { student_id: 1 } });
        expect(result).toEqual(insights);
      });
    });

    describe('generateAIInsights', () => {
      it('should generate new AI insights for a student', async () => {
        const insights = [
          {
            id: 1,
            type: 'learning_pattern',
            title: 'Study Pattern Analysis',
            description: 'Student shows consistent improvement',
            confidence: 0.92,
          },
        ];
        const mockResponse = { data: insights };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.generateAIInsights(1);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/ai-insights/1/generate/');
        expect(result).toEqual(insights);
      });
    });
  });

  describe('Predictive Analytics', () => {
    describe('getPredictions', () => {
      it('should fetch predictions for a student', async () => {
        const predictions = {
          student: 1,
          academicPerformance: {
            nextSemester: 'A-',
            confidence: 0.85,
            factors: ['consistent_attendance', 'high_engagement'],
          },
          riskAssessment: {
            level: 'low',
            factors: ['good_performance', 'regular_attendance'],
          },
        };
        const mockResponse = { data: predictions };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getPredictions(1);

        expect(apiService.get).toHaveBeenCalledWith('/analytics/predictions/1/');
        expect(result).toEqual(predictions);
      });
    });

    describe('generatePredictions', () => {
      it('should generate new predictions for a student', async () => {
        const predictions = {
          student: 1,
          academicPerformance: {
            nextSemester: 'A',
            confidence: 0.90,
            factors: ['excellent_performance', 'high_engagement'],
          },
        };
        const mockResponse = { data: predictions };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.generatePredictions(1);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/predictions/1/generate/');
        expect(result).toEqual(predictions);
      });
    });
  });

  describe('Risk Assessment', () => {
    describe('getRiskAssessment', () => {
      it('should fetch risk assessment for a student', async () => {
        const riskAssessment = {
          student: 1,
          overallRisk: 'low',
          academicRisk: 'low',
          behavioralRisk: 'medium',
          emotionalRisk: 'low',
          recommendations: ['Monitor attendance', 'Provide additional support'],
        };
        const mockResponse = { data: riskAssessment };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.getRiskAssessment(1);

        expect(apiService.get).toHaveBeenCalledWith('/analytics/risk-assessment/1/');
        expect(result).toEqual(riskAssessment);
      });
    });

    describe('generateRiskAssessment', () => {
      it('should generate new risk assessment for a student', async () => {
        const riskAssessment = {
          student: 1,
          overallRisk: 'medium',
          academicRisk: 'medium',
          behavioralRisk: 'low',
          emotionalRisk: 'medium',
          recommendations: ['Schedule counseling', 'Monitor performance'],
        };
        const mockResponse = { data: riskAssessment };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AnalyticsApiService.generateRiskAssessment(1);

        expect(apiService.post).toHaveBeenCalledWith('/analytics/risk-assessment/1/generate/');
        expect(result).toEqual(riskAssessment);
      });
    });
  });

  describe('Trend Analysis', () => {
    it('should fetch trend analysis', async () => {
      const params = {
        student_id: 1,
        subject: 'Mathematics',
        time_period: 'monthly',
        metric: 'performance',
      };
      const trendData = {
        student: 1,
        subject: 'Mathematics',
        trend: 'improving',
        data: [
          { month: 'Sep', value: 0.75 },
          { month: 'Oct', value: 0.78 },
          { month: 'Nov', value: 0.82 },
          { month: 'Dec', value: 0.85 },
        ],
        prediction: 0.88,
      };
      const mockResponse = { data: trendData };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getTrendAnalysis(params);

      expect(apiService.get).toHaveBeenCalledWith('/analytics/trend-analysis/', { params });
      expect(result).toEqual(trendData);
    });
  });

  describe('Comparative Analysis', () => {
    it('should perform comparative analysis', async () => {
      const params = {
        student_ids: [1, 2, 3],
        subjects: ['Mathematics', 'Physics'],
        time_period: 'semester',
      };
      const comparativeData = {
        students: [
          { id: 1, name: 'John Doe', performance: 0.85 },
          { id: 2, name: 'Jane Smith', performance: 0.82 },
          { id: 3, name: 'Bob Johnson', performance: 0.78 },
        ],
        subjects: {
          Mathematics: { average: 0.82, topStudent: 1 },
          Physics: { average: 0.79, topStudent: 2 },
        },
        insights: ['Student 1 shows consistent performance', 'Student 3 needs additional support'],
      };
      const mockResponse = { data: comparativeData };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AnalyticsApiService.getComparativeAnalysis(params);

      expect(apiService.post).toHaveBeenCalledWith('/analytics/comparative-analysis/', params);
      expect(result).toEqual(comparativeData);
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      const error = new Error('Analytics Service Error');
      (apiService.get as jest.Mock).mockRejectedValue(error);

      await expect(AnalyticsApiService.getLearningAnalytics()).rejects.toThrow('Analytics Service Error');
    });

    it('should handle network errors', async () => {
      const networkError = new Error('Network Error');
      (apiService.post as jest.Mock).mockRejectedValue(networkError);

      await expect(AnalyticsApiService.createLearningAnalytics({})).rejects.toThrow('Network Error');
    });

    it('should handle report generation errors', async () => {
      const reportError = new Error('Report Generation Error');
      (apiService.post as jest.Mock).mockRejectedValue(reportError);

      await expect(AnalyticsApiService.generateReport('test', {})).rejects.toThrow('Report Generation Error');
    });
  });
});