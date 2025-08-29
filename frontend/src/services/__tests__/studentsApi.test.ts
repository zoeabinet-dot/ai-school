import { apiService } from '../api';
import StudentsApiService from '../studentsApi';
import { mockStudent, mockPaginatedResponse } from '../../utils/testUtils';

// Mock the API service
jest.mock('../api', () => ({
  apiService: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

describe('StudentsApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getStudents', () => {
    it('should fetch students with default parameters', async () => {
      const mockResponse = mockPaginatedResponse([mockStudent]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.getStudents();

      expect(apiService.get).toHaveBeenCalledWith('/students/', { params: undefined });
      expect(result).toEqual(mockResponse);
    });

    it('should fetch students with custom parameters', async () => {
      const params = {
        page: 1,
        page_size: 10,
        search: 'John',
        grade_level: 10,
        academic_status: 'active',
      };
      const mockResponse = mockPaginatedResponse([mockStudent]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.getStudents(params);

      expect(apiService.get).toHaveBeenCalledWith('/students/', { params });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getStudent', () => {
    it('should fetch a single student by ID', async () => {
      const mockResponse = { data: mockStudent };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.getStudent(1);

      expect(apiService.get).toHaveBeenCalledWith('/students/1/');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createStudent', () => {
    it('should create a new student', async () => {
      const studentData = {
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@example.com',
      };
      const mockResponse = { data: mockStudent };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.createStudent(studentData);

      expect(apiService.post).toHaveBeenCalledWith('/students/', studentData);
      expect(result).toEqual(mockStudent);
    });
  });

  describe('updateStudent', () => {
    it('should update an existing student', async () => {
      const studentData = {
        firstName: 'Jane',
        lastName: 'Smith',
      };
      const mockResponse = { data: mockStudent };
      (apiService.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.updateStudent(1, studentData);

      expect(apiService.put).toHaveBeenCalledWith('/students/1/', studentData);
      expect(result).toEqual(mockStudent);
    });
  });

  describe('deleteStudent', () => {
    it('should delete a student', async () => {
      (apiService.delete as jest.Mock).mockResolvedValue({});

      await StudentsApiService.deleteStudent(1);

      expect(apiService.delete).toHaveBeenCalledWith('/students/1/');
    });
  });

  describe('searchStudents', () => {
    it('should search students by query', async () => {
      const query = 'John Doe';
      const mockResponse = mockPaginatedResponse([mockStudent]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.searchStudents(query);

      expect(apiService.get).toHaveBeenCalledWith('/students/search/', { params: { q: query } });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getStudentDashboard', () => {
    it('should fetch student dashboard data', async () => {
      const dashboardData = {
        recentActivity: [],
        performanceMetrics: {},
        upcomingEvents: [],
      };
      const mockResponse = { data: dashboardData };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await StudentsApiService.getStudentDashboard(1);

      expect(apiService.get).toHaveBeenCalledWith('/students/1/dashboard/');
      expect(result).toEqual(dashboardData);
    });
  });

  describe('Academic Records', () => {
    describe('getAcademicRecords', () => {
      it('should fetch academic records for a student', async () => {
        const records = [
          {
            id: 1,
            subject: 'Mathematics',
            grade: 'A',
            semester: 'Fall 2023',
          },
        ];
        const mockResponse = { data: records };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.getAcademicRecords(1);

        expect(apiService.get).toHaveBeenCalledWith('/students/1/academic-records/');
        expect(result).toEqual(records);
      });
    });

    describe('createAcademicRecord', () => {
      it('should create a new academic record', async () => {
        const recordData = {
          subject: 'Physics',
          grade: 'B+',
          semester: 'Spring 2024',
        };
        const mockResponse = { data: recordData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.createAcademicRecord(1, recordData);

        expect(apiService.post).toHaveBeenCalledWith('/students/1/academic-records/', recordData);
        expect(result).toEqual(recordData);
      });
    });

    describe('updateAcademicRecord', () => {
      it('should update an academic record', async () => {
        const recordData = {
          grade: 'A-',
        };
        const mockResponse = { data: recordData };
        (apiService.put as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.updateAcademicRecord(1, 1, recordData);

        expect(apiService.put).toHaveBeenCalledWith('/students/1/academic-records/1/', recordData);
        expect(result).toEqual(recordData);
      });
    });

    describe('deleteAcademicRecord', () => {
      it('should delete an academic record', async () => {
        (apiService.delete as jest.Mock).mockResolvedValue({});

        await StudentsApiService.deleteAcademicRecord(1, 1);

        expect(apiService.delete).toHaveBeenCalledWith('/students/1/academic-records/1/');
      });
    });
  });

  describe('Student Projects', () => {
    describe('getStudentProjects', () => {
      it('should fetch student projects', async () => {
        const projects = [
          {
            id: 1,
            title: 'Science Fair Project',
            description: 'A project about renewable energy',
            status: 'in_progress',
          },
        ];
        const mockResponse = { data: projects };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.getStudentProjects(1);

        expect(apiService.get).toHaveBeenCalledWith('/students/1/projects/');
        expect(result).toEqual(projects);
      });
    });

    describe('createStudentProject', () => {
      it('should create a new student project', async () => {
        const projectData = {
          title: 'Math Project',
          description: 'Advanced calculus project',
        };
        const mockResponse = { data: projectData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.createStudentProject(1, projectData);

        expect(apiService.post).toHaveBeenCalledWith('/students/1/projects/', projectData);
        expect(result).toEqual(projectData);
      });
    });
  });

  describe('Learning Sessions', () => {
    describe('getLearningSessions', () => {
      it('should fetch learning sessions for a student', async () => {
        const sessions = [
          {
            id: 1,
            sessionType: 'ai_lesson',
            duration: 45,
            engagementLevel: 'high',
          },
        ];
        const mockResponse = { data: sessions };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.getLearningSessions(1);

        expect(apiService.get).toHaveBeenCalledWith('/students/1/learning-sessions/');
        expect(result).toEqual(sessions);
      });
    });

    describe('createLearningSession', () => {
      it('should create a new learning session', async () => {
        const sessionData = {
          sessionType: 'ai_lesson',
          duration: 30,
        };
        const mockResponse = { data: sessionData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.createLearningSession(1, sessionData);

        expect(apiService.post).toHaveBeenCalledWith('/students/1/learning-sessions/', sessionData);
        expect(result).toEqual(sessionData);
      });
    });
  });

  describe('Student Goals', () => {
    describe('getStudentGoals', () => {
      it('should fetch student goals', async () => {
        const goals = [
          {
            id: 1,
            title: 'Improve Math Skills',
            description: 'Achieve A grade in mathematics',
            goalType: 'academic',
            status: 'in_progress',
          },
        ];
        const mockResponse = { data: goals };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.getStudentGoals(1);

        expect(apiService.get).toHaveBeenCalledWith('/students/1/goals/');
        expect(result).toEqual(goals);
      });
    });

    describe('createStudentGoal', () => {
      it('should create a new student goal', async () => {
        const goalData = {
          title: 'Learn Programming',
          description: 'Master Python programming',
          goalType: 'skill',
        };
        const mockResponse = { data: goalData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await StudentsApiService.createStudentGoal(1, goalData);

        expect(apiService.post).toHaveBeenCalledWith('/students/1/goals/', goalData);
        expect(result).toEqual(goalData);
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      const error = new Error('API Error');
      (apiService.get as jest.Mock).mockRejectedValue(error);

      await expect(StudentsApiService.getStudents()).rejects.toThrow('API Error');
    });

    it('should handle network errors', async () => {
      const networkError = new Error('Network Error');
      (apiService.post as jest.Mock).mockRejectedValue(networkError);

      await expect(StudentsApiService.createStudent({})).rejects.toThrow('Network Error');
    });
  });
});