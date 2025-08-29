import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { HelmetProvider } from 'react-helmet-async';
import { toast } from 'react-hot-toast';

// Mock react-hot-toast
jest.mock('react-hot-toast', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    loading: jest.fn(),
    dismiss: jest.fn(),
  },
}));

// Mock API service
jest.mock('../services/api', () => ({
  apiService: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    patch: jest.fn(),
    delete: jest.fn(),
    uploadFile: jest.fn(),
    login: jest.fn(),
    register: jest.fn(),
    logout: jest.fn(),
    getCurrentUser: jest.fn(),
    isAuthenticated: jest.fn(),
    getTokenData: jest.fn(),
    invalidateCache: jest.fn(),
  },
}));

// Mock WebSocket service
jest.mock('../services/websocket', () => ({
  webSocketService: {
    connect: jest.fn(),
    disconnect: jest.fn(),
    on: jest.fn(),
    off: jest.fn(),
    emit: jest.fn(),
    joinChatRoom: jest.fn(),
    leaveChatRoom: jest.fn(),
    sendMessage: jest.fn(),
    isConnected: jest.fn(),
    getConnectionState: jest.fn(),
    cleanup: jest.fn(),
  },
}));

// Mock stores
jest.mock('../store', () => ({
  useAuthStore: jest.fn(),
  useStudentsStore: jest.fn(),
  useAILessonsStore: jest.fn(),
  useAnalyticsStore: jest.fn(),
  useNotificationsStore: jest.fn(),
  useChatStore: jest.fn(),
  useDashboardStore: jest.fn(),
}));

// Create a custom render function that includes providers
export const renderWithProviders = (
  ui: React.ReactElement,
  {
    preloadedState = {},
    store = {},
    ...renderOptions
  } = {}
) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  const Wrapper = ({ children }: { children: React.ReactNode }) => {
    return React.createElement(HelmetProvider, null,
      React.createElement(QueryClientProvider, { client: queryClient },
        React.createElement(BrowserRouter, null, children)
      )
    );
  };

  return {
    store,
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
};

// Mock data for testing
export const mockUser = {
  id: 1,
  email: 'test@example.com',
  firstName: 'John',
  lastName: 'Doe',
  role: 'admin',
  isActive: true,
  dateJoined: '2023-01-01T00:00:00Z',
  lastLogin: '2023-12-01T00:00:00Z',
  profileImage: null,
  phoneNumber: '+1234567890',
  dateOfBirth: '1990-01-01',
  gender: 'male',
  address: {
    street: '123 Main St',
    city: 'Addis Ababa',
    state: 'Addis Ababa',
    country: 'Ethiopia',
    postalCode: '1000',
    coordinates: {
      latitude: 9.145,
      longitude: 40.4897,
    },
  },
  preferences: {
    notifications: {
      email: true,
      push: true,
      sms: false,
    },
    privacy: {
      profileVisibility: 'public',
      academicRecordVisibility: 'family',
      dataSharing: {
        analytics: true,
        research: false,
        thirdParty: false,
      },
    },
    accessibility: {
      fontSize: 'medium',
      colorBlindness: 'none',
      screenReader: false,
    },
    theme: 'light',
    language: 'en',
  },
  permissions: ['view_students', 'edit_students', 'view_analytics'],
  metadata: {},
};

export const mockStudent = {
  id: 1,
  user: mockUser,
  studentId: 'STU001',
  gradeLevel: 10,
  academicStatus: 'active',
  enrollmentDate: '2023-09-01',
  graduationDate: '2026-06-30',
  learningStyle: {
    visual: 0.7,
    auditory: 0.3,
    kinesthetic: 0.5,
    reading: 0.8,
    social: 0.6,
  },
  emergencyContacts: [
    {
      name: 'Jane Doe',
      relationship: 'parent',
      phone: '+1234567890',
      email: 'jane@example.com',
      isPrimary: true,
    },
  ],
  academicRecords: [],
  projects: [],
  learningSessions: [],
  goals: [],
  createdAt: '2023-09-01T00:00:00Z',
  updatedAt: '2023-12-01T00:00:00Z',
};

export const mockAILesson = {
  id: 1,
  title: 'Introduction to Machine Learning',
  subject: 'Computer Science',
  gradeLevel: 10,
  difficultyLevel: 'intermediate',
  content: 'This lesson covers the basics of machine learning...',
  learningObjectives: [
    'Understand basic ML concepts',
    'Identify different types of ML algorithms',
    'Apply ML concepts to real-world problems',
  ],
  estimatedDuration: 45,
  prerequisites: ['Basic programming knowledge'],
  materials: [
    {
      type: 'video',
      title: 'ML Introduction Video',
      url: 'https://example.com/video.mp4',
      description: 'Introduction to machine learning concepts',
    },
  ],
  assessments: [
    {
      type: 'quiz',
      title: 'ML Basics Quiz',
      questions: [
        {
          type: 'multiple_choice',
          question: 'What is machine learning?',
          options: ['A type of computer', 'A programming language', 'A subset of AI', 'A database system'],
          correctAnswer: 2,
        },
      ],
    },
  ],
  aiModel: 'gpt-4',
  conversationHistory: [],
  createdAt: '2023-12-01T00:00:00Z',
  updatedAt: '2023-12-01T00:00:00Z',
};

export const mockLearningAnalytics = {
  id: 1,
  student: mockStudent,
  subject: 'Mathematics',
  timeSpent: 120,
  completionRate: 0.85,
  engagementScore: 0.78,
  performanceScore: 0.82,
  learningPath: 'adaptive',
  sessionDate: '2023-12-01',
  metadata: {
    difficultyLevel: 'intermediate',
    topicsCovered: ['algebra', 'calculus'],
    interactions: 45,
  },
  createdAt: '2023-12-01T00:00:00Z',
};

export const mockWebcamSession = {
  id: 1,
  student: mockStudent,
  startTime: '2023-12-01T09:00:00Z',
  endTime: '2023-12-01T10:00:00Z',
  status: 'completed',
  recordingUrl: 'https://example.com/recording.mp4',
  privacySettings: {
    blurFaces: true,
    recordAudio: false,
    storeLocally: true,
    retentionPeriod: 30,
  },
  frameAnalysis: [],
  behaviorEvents: [],
  createdAt: '2023-12-01T00:00:00Z',
};

export const mockFamily = {
  id: 1,
  name: 'Doe Family',
  primaryContact: {
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    relationship: 'father',
  },
  address: {
    street: '123 Main St',
    city: 'Addis Ababa',
    state: 'Addis Ababa',
    country: 'Ethiopia',
    postalCode: '1000',
  },
  members: [],
  students: [],
  createdAt: '2023-01-01T00:00:00Z',
  updatedAt: '2023-12-01T00:00:00Z',
};

export const mockStaff = {
  id: 1,
  user: mockUser,
  employeeId: 'EMP001',
  department: 'Teaching',
  position: 'Teacher',
  hireDate: '2023-01-01',
  salary: 50000,
  qualifications: ['Bachelor of Education', 'Teaching License'],
  specializations: ['Mathematics', 'Physics'],
  assignments: [],
  schedule: [],
  performance: [],
  createdAt: '2023-01-01T00:00:00Z',
  updatedAt: '2023-12-01T00:00:00Z',
};

export const mockLesson = {
  id: 1,
  title: 'Advanced Mathematics',
  subject: 'Mathematics',
  gradeLevel: 10,
  description: 'Advanced mathematical concepts and problem-solving',
  objectives: [
    'Master advanced algebra',
    'Understand calculus fundamentals',
    'Apply mathematical concepts',
  ],
  duration: 60,
  materials: [],
  assessments: [],
  teacher: mockStaff,
  students: [mockStudent],
  createdAt: '2023-09-01T00:00:00Z',
  updatedAt: '2023-12-01T00:00:00Z',
};

// Mock API responses
export const mockApiResponse = <T>(data: T) => ({
  data,
  status: 200,
  statusText: 'OK',
  headers: {},
  config: {},
});

export const mockPaginatedResponse = <T>(data: T[], count: number = data.length) => ({
  data: {
    results: data,
    count,
    next: null,
    previous: null,
  },
  status: 200,
  statusText: 'OK',
  headers: {},
  config: {},
});

// Test utilities
export const waitForLoadingToFinish = () =>
  waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

export const waitForErrorToAppear = () =>
  waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });

export const waitForSuccessMessage = () =>
  waitFor(() => {
    expect(toast.success).toHaveBeenCalled();
  });

export const waitForErrorMessage = () =>
  waitFor(() => {
    expect(toast.error).toHaveBeenCalled();
  });

// Custom matchers
export const expectElementToBeInDocument = (element: HTMLElement) => {
  expect(element).toBeInTheDocument();
};

export const expectElementNotToBeInDocument = (element: HTMLElement) => {
  expect(element).not.toBeInTheDocument();
};

export const expectTextToBeInDocument = (text: string) => {
  expect(screen.getByText(text)).toBeInTheDocument();
};

export const expectTextNotToBeInDocument = (text: string) => {
  expect(screen.queryByText(text)).not.toBeInTheDocument();
};

// Form testing utilities
export const fillFormField = (name: string, value: string) => {
  const field = screen.getByLabelText(name) || screen.getByPlaceholderText(name);
  fireEvent.change(field, { target: { value } });
};

export const submitForm = (form: HTMLElement) => {
  fireEvent.submit(form);
};

export const clickButton = (text: string) => {
  const button = screen.getByRole('button', { name: text });
  fireEvent.click(button);
};

export const clickLink = (text: string) => {
  const link = screen.getByRole('link', { name: text });
  fireEvent.click(link);
};

// Navigation testing utilities
export const expectCurrentPath = (path: string) => {
  expect(window.location.pathname).toBe(path);
};

// Mock Intersection Observer
export const mockIntersectionObserver = () => {
  const mockIntersectionObserver = jest.fn();
  mockIntersectionObserver.mockReturnValue({
    observe: () => null,
    unobserve: () => null,
    disconnect: () => null,
  });
  window.IntersectionObserver = mockIntersectionObserver;
};

// Mock ResizeObserver
export const mockResizeObserver = () => {
  const mockResizeObserver = jest.fn();
  mockResizeObserver.mockReturnValue({
    observe: () => null,
    unobserve: () => null,
    disconnect: () => null,
  });
  window.ResizeObserver = mockResizeObserver;
};

// Mock matchMedia
export const mockMatchMedia = () => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
};

// Setup global mocks
beforeAll(() => {
  mockIntersectionObserver();
  mockResizeObserver();
  mockMatchMedia();
});

// Cleanup after each test
afterEach(() => {
  jest.clearAllMocks();
  jest.clearAllTimers();
});