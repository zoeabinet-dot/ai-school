import { apiService } from '../api';
import AITeacherApiService from '../aiTeacherApi';
import { mockAILesson, mockPaginatedResponse } from '../../utils/testUtils';

// Mock the API service
jest.mock('../api', () => ({
  apiService: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

describe('AITeacherApiService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAILessons', () => {
    it('should fetch AI lessons with default parameters', async () => {
      const mockResponse = mockPaginatedResponse([mockAILesson]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.getAILessons();

      expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/lessons/', { params: undefined });
      expect(result).toEqual(mockResponse);
    });

    it('should fetch AI lessons with custom parameters', async () => {
      const params = {
        page: 1,
        page_size: 10,
        subject: 'Computer Science',
        grade_level: 10,
        difficulty_level: 'intermediate',
      };
      const mockResponse = mockPaginatedResponse([mockAILesson]);
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.getAILessons(params);

      expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/lessons/', { params });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getAILesson', () => {
    it('should fetch a single AI lesson by ID', async () => {
      const mockResponse = { data: mockAILesson };
      (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.getAILesson(1);

      expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/lessons/1/');
      expect(result).toEqual(mockAILesson);
    });
  });

  describe('createAILesson', () => {
    it('should create a new AI lesson', async () => {
      const lessonData = {
        title: 'Introduction to AI',
        subject: 'Computer Science',
        gradeLevel: 10,
        difficultyLevel: 'beginner',
      };
      const mockResponse = { data: mockAILesson };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.createAILesson(lessonData);

      expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/lessons/', lessonData);
      expect(result).toEqual(mockAILesson);
    });
  });

  describe('updateAILesson', () => {
    it('should update an existing AI lesson', async () => {
      const lessonData = {
        title: 'Advanced AI Concepts',
        difficultyLevel: 'advanced',
      };
      const mockResponse = { data: mockAILesson };
      (apiService.put as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.updateAILesson(1, lessonData);

      expect(apiService.put).toHaveBeenCalledWith('/ai-teacher/lessons/1/', lessonData);
      expect(result).toEqual(mockAILesson);
    });
  });

  describe('deleteAILesson', () => {
    it('should delete an AI lesson', async () => {
      (apiService.delete as jest.Mock).mockResolvedValue({});

      await AITeacherApiService.deleteAILesson(1);

      expect(apiService.delete).toHaveBeenCalledWith('/ai-teacher/lessons/1/');
    });
  });

  describe('generateAILesson', () => {
    it('should generate an AI lesson from prompt', async () => {
      const prompt = 'Create a lesson about machine learning basics';
      const mockResponse = { data: mockAILesson };
      (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await AITeacherApiService.generateAILesson(prompt);

      expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/generate-lesson/', { prompt });
      expect(result).toEqual(mockAILesson);
    });
  });

  describe('AI Conversations', () => {
    describe('getConversations', () => {
      it('should fetch all conversations', async () => {
        const conversations = [
          {
            id: 1,
            studentId: 1,
            status: 'active',
            createdAt: '2023-12-01T00:00:00Z',
          },
        ];
        const mockResponse = { data: conversations };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getConversations();

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/conversations/', { params: {} });
        expect(result).toEqual(conversations);
      });

      it('should fetch conversations for a specific student', async () => {
        const conversations = [
          {
            id: 1,
            studentId: 1,
            status: 'active',
            createdAt: '2023-12-01T00:00:00Z',
          },
        ];
        const mockResponse = { data: conversations };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getConversations(1);

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/conversations/', { params: { student_id: 1 } });
        expect(result).toEqual(conversations);
      });
    });

    describe('getConversation', () => {
      it('should fetch a single conversation by ID', async () => {
        const conversation = {
          id: 1,
          studentId: 1,
          status: 'active',
          messages: [],
        };
        const mockResponse = { data: conversation };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getConversation(1);

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/conversations/1/');
        expect(result).toEqual(conversation);
      });
    });

    describe('createConversation', () => {
      it('should create a new conversation', async () => {
        const conversationData = {
          studentId: 1,
          topic: 'Mathematics',
        };
        const mockResponse = { data: conversationData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.createConversation(conversationData);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/conversations/', conversationData);
        expect(result).toEqual(conversationData);
      });
    });
  });

  describe('Conversation Messages', () => {
    describe('getConversationMessages', () => {
      it('should fetch messages for a conversation', async () => {
        const messages = [
          {
            id: 1,
            content: 'Hello, how can I help you today?',
            senderType: 'ai',
            timestamp: '2023-12-01T00:00:00Z',
          },
        ];
        const mockResponse = { data: messages };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getConversationMessages(1);

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/conversations/1/messages/');
        expect(result).toEqual(messages);
      });
    });

    describe('sendMessage', () => {
      it('should send a message in a conversation', async () => {
        const messageData = {
          content: 'I need help with math',
          senderType: 'student',
        };
        const mockResponse = { data: messageData };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.sendMessage(1, messageData);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/conversations/1/messages/', messageData);
        expect(result).toEqual(messageData);
      });
    });
  });

  describe('Speech Processing', () => {
    describe('speechToText', () => {
      it('should convert speech to text', async () => {
        const audioFile = new File([''], 'test.wav', { type: 'audio/wav' });
        const mockResponse = { data: { text: 'Hello world' } };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.speechToText(audioFile);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/speech-to-text/', expect.any(FormData));
        expect(result).toEqual({ text: 'Hello world' });
      });
    });

    describe('textToSpeech', () => {
      it('should convert text to speech', async () => {
        const text = 'Hello, this is a test message';
        const voice = 'en-US-Standard-A';
        const mockResponse = { data: { audio_url: 'https://example.com/audio.mp3' } };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.textToSpeech(text, voice);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/text-to-speech/', { text, voice });
        expect(result).toEqual({ audio_url: 'https://example.com/audio.mp3' });
      });
    });
  });

  describe('AI Recommendations', () => {
    describe('getRecommendations', () => {
      it('should fetch AI recommendations for a student', async () => {
        const recommendations = [
          {
            id: 1,
            type: 'lesson',
            title: 'Advanced Mathematics',
            description: 'Recommended based on your performance',
            confidence: 0.85,
          },
        ];
        const mockResponse = { data: recommendations };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getRecommendations(1);

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/recommendations/1/');
        expect(result).toEqual(recommendations);
      });
    });

    describe('generateRecommendations', () => {
      it('should generate new AI recommendations', async () => {
        const recommendations = [
          {
            id: 1,
            type: 'lesson',
            title: 'Machine Learning Basics',
            description: 'New recommendation generated',
            confidence: 0.92,
          },
        ];
        const mockResponse = { data: recommendations };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.generateRecommendations(1);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/recommendations/1/generate/');
        expect(result).toEqual(recommendations);
      });
    });
  });

  describe('Behavioral Analysis', () => {
    describe('analyzeBehavior', () => {
      it('should analyze student behavior', async () => {
        const behaviorData = {
          sessionDuration: 45,
          engagementLevel: 'high',
          interactions: 25,
        };
        const analysisResult = {
          attentionScore: 0.85,
          engagementTrend: 'improving',
          recommendations: ['Take more breaks', 'Increase interaction'],
        };
        const mockResponse = { data: analysisResult };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.analyzeBehavior(1, behaviorData);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/behavior-analysis/1/', behaviorData);
        expect(result).toEqual(analysisResult);
      });
    });

    describe('getBehaviorReport', () => {
      it('should fetch behavior report for a student', async () => {
        const report = {
          studentId: 1,
          period: 'weekly',
          attentionScore: 0.82,
          engagementTrend: 'stable',
          recommendations: ['Consider shorter sessions'],
        };
        const mockResponse = { data: report };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getBehaviorReport(1, 'weekly');

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/behavior-analysis/1/report/', { params: { date_range: 'weekly' } });
        expect(result).toEqual(report);
      });
    });
  });

  describe('AI Model Management', () => {
    describe('getAIModels', () => {
      it('should fetch available AI models', async () => {
        const models = [
          {
            id: 'gpt-4',
            name: 'GPT-4',
            type: 'language_model',
            status: 'active',
          },
        ];
        const mockResponse = { data: models };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getAIModels();

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/models/');
        expect(result).toEqual(models);
      });
    });

    describe('trainAIModel', () => {
      it('should train an AI model', async () => {
        const trainingData = {
          dataset: 'student_responses',
          epochs: 100,
          batchSize: 32,
        };
        const trainingResult = {
          modelId: 'custom-model-1',
          status: 'training',
          progress: 0.25,
        };
        const mockResponse = { data: trainingResult };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.trainAIModel('custom-model-1', trainingData);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/models/custom-model-1/train/', trainingData);
        expect(result).toEqual(trainingResult);
      });
    });

    describe('deployAIModel', () => {
      it('should deploy an AI model', async () => {
        const deploymentResult = {
          modelId: 'custom-model-1',
          status: 'deployed',
          endpoint: 'https://api.example.com/model/custom-model-1',
        };
        const mockResponse = { data: deploymentResult };
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.deployAIModel('custom-model-1');

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/models/custom-model-1/deploy/');
        expect(result).toEqual(deploymentResult);
      });
    });
  });

  describe('AI Insights', () => {
    describe('getAIInsights', () => {
      it('should fetch AI insights for a student', async () => {
        const insights = [
          {
            id: 1,
            type: 'learning_pattern',
            title: 'Optimal Learning Time',
            description: 'Student performs best in morning sessions',
            confidence: 0.88,
          },
        ];
        const mockResponse = { data: insights };
        (apiService.get as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.getAIInsights(1);

        expect(apiService.get).toHaveBeenCalledWith('/ai-teacher/insights/1/');
        expect(result).toEqual(insights);
      });
    });

    describe('generateAIInsights', () => {
      it('should generate new AI insights', async () => {
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
        (apiService.post as jest.Mock).mockResolvedValue(mockResponse);

        const result = await AITeacherApiService.generateAIInsights(1);

        expect(apiService.post).toHaveBeenCalledWith('/ai-teacher/insights/1/generate/');
        expect(result).toEqual(insights);
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      const error = new Error('AI Service Error');
      (apiService.get as jest.Mock).mockRejectedValue(error);

      await expect(AITeacherApiService.getAILessons()).rejects.toThrow('AI Service Error');
    });

    it('should handle network errors', async () => {
      const networkError = new Error('Network Error');
      (apiService.post as jest.Mock).mockRejectedValue(networkError);

      await expect(AITeacherApiService.createAILesson({})).rejects.toThrow('Network Error');
    });

    it('should handle file upload errors', async () => {
      const uploadError = new Error('Upload Error');
      const audioFile = new File([''], 'test.wav', { type: 'audio/wav' });
      (apiService.post as jest.Mock).mockRejectedValue(uploadError);

      await expect(AITeacherApiService.speechToText(audioFile)).rejects.toThrow('Upload Error');
    });
  });
});