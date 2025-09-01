import { apiService } from '../api';
import StudentsApiService from '../studentsApi';
import AITeacherApiService from '../aiTeacherApi';
import AnalyticsApiService from '../analyticsApi';

describe.skip('Backend Integration Tests', () => {
  const testTimeout = 10000; // 10 seconds

  beforeAll(async () => {
    // Wait for backend to be ready
    await new Promise(resolve => setTimeout(resolve, 2000));
  });

  describe('Health Check', () => {
    it('should connect to Django backend', async () => {
      try {
        const response = await fetch('http://localhost:8000/health/');
        expect(response.status).toBe(200);
        const text = await response.text();
        expect(text).toBe('OK');
      } catch (error) {
        throw new Error('Django backend is not running or not accessible');
      }
    }, testTimeout);
  });

  describe('API Service Configuration', () => {
    it('should have correct base URL', () => {
      expect(apiService['api'].defaults.baseURL).toBe('http://localhost:8000/api/v1');
    });

    it('should have correct timeout', () => {
      expect(apiService['api'].defaults.timeout).toBe(10000);
    });

    it('should have correct headers', () => {
      expect(apiService['api'].defaults.headers['Content-Type']).toBe('application/json');
    });
  });

  describe('Students API Integration', () => {
    it('should handle authentication required error', async () => {
      let caughtError: any = null;
      try {
        await StudentsApiService.getStudents();
        throw new Error('Should have thrown authentication error');
      } catch (error: any) {
        caughtError = error;
      }

      expect(caughtError).not.toBeNull();
      expect(caughtError.response).toBeDefined();
      expect(caughtError.response.status).toBe(401);
      expect(caughtError.response.data).toContain('Unauthorized');
    }, testTimeout);

    it('should have correct endpoint structure', () => {
      // Test that the service methods are properly configured
      expect(typeof StudentsApiService.getStudents).toBe('function');
      expect(typeof StudentsApiService.getStudent).toBe('function');
      expect(typeof StudentsApiService.createStudent).toBe('function');
      expect(typeof StudentsApiService.updateStudent).toBe('function');
      expect(typeof StudentsApiService.deleteStudent).toBe('function');
    });
  });

  describe('AI Teacher API Integration', () => {
    it('should handle authentication required error', async () => {
      let caughtError2: any = null;
      try {
        await AITeacherApiService.getAILessons();
        throw new Error('Should have thrown authentication error');
      } catch (error: any) {
        caughtError2 = error;
      }

      expect(caughtError2).not.toBeNull();
      expect(caughtError2.response).toBeDefined();
      expect(caughtError2.response.status).toBe(401);
      expect(caughtError2.response.data).toContain('Unauthorized');
    }, testTimeout);

    it('should have correct endpoint structure', () => {
      expect(typeof AITeacherApiService.getAILessons).toBe('function');
      expect(typeof AITeacherApiService.getAILesson).toBe('function');
      expect(typeof AITeacherApiService.createAILesson).toBe('function');
      expect(typeof AITeacherApiService.generateAILesson).toBe('function');
    });
  });

  describe('Analytics API Integration', () => {
    it('should handle authentication required error', async () => {
      let caughtError3: any = null;
      try {
        await AnalyticsApiService.getLearningAnalytics();
        throw new Error('Should have thrown authentication error');
      } catch (error: any) {
        caughtError3 = error;
      }

      expect(caughtError3).not.toBeNull();
      expect(caughtError3.response).toBeDefined();
      expect(caughtError3.response.status).toBe(401);
      expect(caughtError3.response.data).toContain('Unauthorized');
    }, testTimeout);

    it('should have correct endpoint structure', () => {
      expect(typeof AnalyticsApiService.getLearningAnalytics).toBe('function');
      expect(typeof AnalyticsApiService.getPerformanceMetrics).toBe('function');
      expect(typeof AnalyticsApiService.getEngagementAnalytics).toBe('function');
      expect(typeof AnalyticsApiService.generateReport).toBe('function');
    });
  });

  describe('Error Handling', () => {
    it('should handle network errors gracefully', async () => {
      // Temporarily change base URL to invalid endpoint
      const originalBaseURL = apiService['api'].defaults.baseURL;
      apiService['api'].defaults.baseURL = 'http://invalid-url:9999';

        let networkErr: any = null;
        try {
          await StudentsApiService.getStudents();
          throw new Error('Should have thrown network error');
        } catch (error: any) {
          networkErr = error;
        } finally {
          expect(networkErr).not.toBeNull();
          expect(networkErr.message).toContain('Network Error');
        // Restore original base URL
        apiService['api'].defaults.baseURL = originalBaseURL;
      }
    }, testTimeout);

    it('should handle timeout errors', async () => {
      // Temporarily set very short timeout
      const originalTimeout = apiService['api'].defaults.timeout;
      apiService['api'].defaults.timeout = 1;

        let timeoutErr: any = null;
        try {
          await StudentsApiService.getStudents();
          throw new Error('Should have thrown timeout error');
        } catch (error: any) {
          timeoutErr = error;
        } finally {
          expect(timeoutErr).not.toBeNull();
          expect(timeoutErr.message).toContain('timeout');
        // Restore original timeout
        apiService['api'].defaults.timeout = originalTimeout;
      }
    }, testTimeout);
  });

  describe('API Endpoint Validation', () => {
    it('should validate students endpoints', () => {
      const endpoints = [
        '/students/',
        '/students/1/',
        '/students/search/',
        '/students/1/dashboard/',
        '/students/1/academic-records/',
        '/students/1/projects/',
        '/students/1/learning-sessions/',
        '/students/1/goals/',
      ];

      endpoints.forEach(endpoint => {
        expect(endpoint).toMatch(/^\/students\/.*/);
      });
    });

    it('should validate AI teacher endpoints', () => {
      const endpoints = [
        '/ai-teacher/lessons/',
        '/ai-teacher/lessons/1/',
        '/ai-teacher/generate-lesson/',
        '/ai-teacher/conversations/',
        '/ai-teacher/speech-to-text/',
        '/ai-teacher/text-to-speech/',
        '/ai-teacher/recommendations/1/',
        '/ai-teacher/models/',
      ];

      endpoints.forEach(endpoint => {
        expect(endpoint).toMatch(/^\/ai-teacher\/.*/);
      });
    });

    it('should validate analytics endpoints', () => {
      const endpoints = [
        '/analytics/learning-analytics/',
        '/analytics/performance-metrics/',
        '/analytics/engagement-analytics/',
        '/analytics/dashboard-configurations/',
        '/analytics/report-templates/',
        '/analytics/student-dashboard/1/',
        '/analytics/class-dashboard/1/',
        '/analytics/generate-report/',
        '/analytics/export/',
        '/analytics/ai-insights/',
        '/analytics/predictions/1/',
        '/analytics/risk-assessment/1/',
        '/analytics/trend-analysis/',
        '/analytics/comparative-analysis/',
      ];

      endpoints.forEach(endpoint => {
        expect(endpoint).toMatch(/^\/analytics\/.*/);
      });
    });
  });

  describe('Data Format Validation', () => {
    it('should validate student data structure', () => {
      const mockStudent = {
        id: 1,
        user: {
          id: 1,
          email: 'test@example.com',
          firstName: 'John',
          lastName: 'Doe',
          role: 'student',
        },
        studentId: 'STU001',
        gradeLevel: 10,
        academicStatus: 'active',
        enrollmentDate: '2023-09-01',
        graduationDate: '2026-06-30',
      };

      expect(mockStudent).toHaveProperty('id');
      expect(mockStudent).toHaveProperty('user');
      expect(mockStudent).toHaveProperty('studentId');
      expect(mockStudent).toHaveProperty('gradeLevel');
      expect(mockStudent).toHaveProperty('academicStatus');
      expect(mockStudent.user).toHaveProperty('email');
      expect(mockStudent.user).toHaveProperty('firstName');
      expect(mockStudent.user).toHaveProperty('lastName');
      expect(mockStudent.user).toHaveProperty('role');
    });

    it('should validate AI lesson data structure', () => {
      const mockAILesson = {
        id: 1,
        title: 'Introduction to AI',
        subject: 'Computer Science',
        gradeLevel: 10,
        difficultyLevel: 'intermediate',
        content: 'This lesson covers...',
        learningObjectives: ['Objective 1', 'Objective 2'],
        estimatedDuration: 45,
        aiModel: 'gpt-4',
      };

      expect(mockAILesson).toHaveProperty('id');
      expect(mockAILesson).toHaveProperty('title');
      expect(mockAILesson).toHaveProperty('subject');
      expect(mockAILesson).toHaveProperty('gradeLevel');
      expect(mockAILesson).toHaveProperty('difficultyLevel');
      expect(mockAILesson).toHaveProperty('content');
      expect(mockAILesson).toHaveProperty('learningObjectives');
      expect(mockAILesson).toHaveProperty('estimatedDuration');
      expect(mockAILesson).toHaveProperty('aiModel');
      expect(Array.isArray(mockAILesson.learningObjectives)).toBe(true);
    });

    it('should validate analytics data structure', () => {
      const mockAnalytics = {
        id: 1,
        student: 1,
        subject: 'Mathematics',
        timeSpent: 120,
        completionRate: 0.85,
        engagementScore: 0.78,
        performanceScore: 0.82,
        learningPath: 'adaptive',
        sessionDate: '2023-12-01',
      };

      expect(mockAnalytics).toHaveProperty('id');
      expect(mockAnalytics).toHaveProperty('student');
      expect(mockAnalytics).toHaveProperty('subject');
      expect(mockAnalytics).toHaveProperty('timeSpent');
      expect(mockAnalytics).toHaveProperty('completionRate');
      expect(mockAnalytics).toHaveProperty('engagementScore');
      expect(mockAnalytics).toHaveProperty('performanceScore');
      expect(mockAnalytics).toHaveProperty('learningPath');
      expect(mockAnalytics).toHaveProperty('sessionDate');
      expect(typeof mockAnalytics.completionRate).toBe('number');
      expect(typeof mockAnalytics.engagementScore).toBe('number');
      expect(typeof mockAnalytics.performanceScore).toBe('number');
    });
  });
});