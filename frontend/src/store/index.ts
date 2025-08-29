import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { 
  User, 
  AuthState, 
  Student, 
  AILesson, 
  LearningAnalytics, 
  WebcamSession,
  Family,
  Staff,
  Lesson,
  Notification,
  ChatRoom,
  ChatMessage,
  DashboardData,
  PaginationState,
  LoadingState
} from '../types';
import { apiService } from '../services/api';
import { webSocketService } from '../services/websocket';

// Auth Store
interface AuthStore extends AuthState {
  login: (credentials: { email: string; password: string; role: string }) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,

        login: async (credentials) => {
          set({ isLoading: true, error: null });
          try {
            const response = await apiService.login(credentials);
            set({
              user: response.user,
              token: response.access,
              refreshToken: response.refresh,
              isAuthenticated: true,
              isLoading: false,
            });
            
            // Connect WebSocket after successful login
            await webSocketService.connect(response.access);
          } catch (error: any) {
            set({
              error: error.message || 'Login failed',
              isLoading: false,
            });
            throw error;
          }
        },

        register: async (userData) => {
          set({ isLoading: true, error: null });
          try {
            const response = await apiService.register(userData);
            set({
              user: response.user,
              token: response.access,
              refreshToken: response.refresh,
              isAuthenticated: true,
              isLoading: false,
            });
            
            await webSocketService.connect(response.access);
          } catch (error: any) {
            set({
              error: error.message || 'Registration failed',
              isLoading: false,
            });
            throw error;
          }
        },

        logout: async () => {
          set({ isLoading: true });
          try {
            await apiService.logout();
          } catch (error) {
            console.error('Logout error:', error);
          } finally {
            webSocketService.disconnect();
            set({
              user: null,
              token: null,
              refreshToken: null,
              isAuthenticated: false,
              isLoading: false,
              error: null,
            });
          }
        },

        checkAuth: async () => {
          if (!apiService.isAuthenticated()) {
            set({
              user: null,
              token: null,
              refreshToken: null,
              isAuthenticated: false,
              isLoading: false,
            });
            return;
          }

          set({ isLoading: true });
          try {
            const user = await apiService.getCurrentUser();
            set({
              user,
              isAuthenticated: true,
              isLoading: false,
            });
            
            await webSocketService.connect();
          } catch (error: any) {
            set({
              user: null,
              token: null,
              refreshToken: null,
              isAuthenticated: false,
              isLoading: false,
              error: error.message,
            });
          }
        },

        clearError: () => set({ error: null }),
      }),
      {
        name: 'auth-storage',
        partialize: (state) => ({
          token: state.token,
          refreshToken: state.refreshToken,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    ),
    { name: 'auth-store' }
  )
);

// Students Store
interface StudentsStore {
  students: Student[];
  currentStudent: Student | null;
  pagination: PaginationState;
  loading: LoadingState;
  
  fetchStudents: (params?: any) => Promise<void>;
  fetchStudent: (id: number) => Promise<void>;
  createStudent: (data: Partial<Student>) => Promise<void>;
  updateStudent: (id: number, data: Partial<Student>) => Promise<void>;
  deleteStudent: (id: number) => Promise<void>;
  searchStudents: (query: string) => Promise<void>;
  clearStudents: () => void;
}

export const useStudentsStore = create<StudentsStore>()(
  devtools(
    (set, get) => ({
      students: [],
      currentStudent: null,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0,
        totalPages: 0,
      },
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchStudents: async (params = {}) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/students/', { params });
          set({
            students: response.results,
            pagination: {
              page: params.page || 1,
              pageSize: params.page_size || 10,
              total: response.count,
              totalPages: Math.ceil(response.count / (params.page_size || 10)),
            },
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      fetchStudent: async (id) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const student = await apiService.get(`/students/${id}/`);
          set({
            currentStudent: student,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      createStudent: async (data) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.post('/students/', data);
          await get().fetchStudents();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      updateStudent: async (id, data) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.put(`/students/${id}/`, data);
          await get().fetchStudents();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      deleteStudent: async (id) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.delete(`/students/${id}/`);
          await get().fetchStudents();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      searchStudents: async (query) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/students/search/', {
            params: { q: query },
          });
          set({
            students: response.results,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      clearStudents: () => {
        set({
          students: [],
          currentStudent: null,
          pagination: {
            page: 1,
            pageSize: 10,
            total: 0,
            totalPages: 0,
          },
        });
      },
    }),
    { name: 'students-store' }
  )
);

// AI Lessons Store
interface AILessonsStore {
  lessons: AILesson[];
  currentLesson: AILesson | null;
  pagination: PaginationState;
  loading: LoadingState;
  
  fetchLessons: (params?: any) => Promise<void>;
  fetchLesson: (id: number) => Promise<void>;
  createLesson: (data: Partial<AILesson>) => Promise<void>;
  updateLesson: (id: number, data: Partial<AILesson>) => Promise<void>;
  deleteLesson: (id: number) => Promise<void>;
  generateLesson: (prompt: string) => Promise<void>;
  clearLessons: () => void;
}

export const useAILessonsStore = create<AILessonsStore>()(
  devtools(
    (set, get) => ({
      lessons: [],
      currentLesson: null,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0,
        totalPages: 0,
      },
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchLessons: async (params = {}) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/ai-teacher/lessons/', { params });
          set({
            lessons: response.results,
            pagination: {
              page: params.page || 1,
              pageSize: params.page_size || 10,
              total: response.count,
              totalPages: Math.ceil(response.count / (params.page_size || 10)),
            },
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      fetchLesson: async (id) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const lesson = await apiService.get(`/ai-teacher/lessons/${id}/`);
          set({
            currentLesson: lesson,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      createLesson: async (data) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.post('/ai-teacher/lessons/', data);
          await get().fetchLessons();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      updateLesson: async (id, data) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.put(`/ai-teacher/lessons/${id}/`, data);
          await get().fetchLessons();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      deleteLesson: async (id) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          await apiService.delete(`/ai-teacher/lessons/${id}/`);
          await get().fetchLessons();
          set({ loading: { ...get().loading, isLoading: false } });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      generateLesson: async (prompt) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const lesson = await apiService.post('/ai-teacher/generate-lesson/', {
            prompt,
          });
          set({
            currentLesson: lesson,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      clearLessons: () => {
        set({
          lessons: [],
          currentLesson: null,
          pagination: {
            page: 1,
            pageSize: 10,
            total: 0,
            totalPages: 0,
          },
        });
      },
    }),
    { name: 'ai-lessons-store' }
  )
);

// Analytics Store
interface AnalyticsStore {
  analytics: LearningAnalytics[];
  currentAnalytics: LearningAnalytics | null;
  loading: LoadingState;
  
  fetchAnalytics: (params?: any) => Promise<void>;
  fetchAnalyticsById: (id: number) => Promise<void>;
  generateReport: (params: any) => Promise<void>;
  exportData: (format: string, params: any) => Promise<void>;
  clearAnalytics: () => void;
}

export const useAnalyticsStore = create<AnalyticsStore>()(
  devtools(
    (set, get) => ({
      analytics: [],
      currentAnalytics: null,
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchAnalytics: async (params = {}) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/analytics/learning-analytics/', { params });
          set({
            analytics: response.results,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      fetchAnalyticsById: async (id) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const analytics = await apiService.get(`/analytics/learning-analytics/${id}/`);
          set({
            currentAnalytics: analytics,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      generateReport: async (params) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const report = await apiService.post('/analytics/generate-report/', params);
          set({ loading: { ...get().loading, isLoading: false } });
          return report;
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      exportData: async (format, params) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const data = await apiService.get('/analytics/export/', {
            params: { format, ...params },
          });
          set({ loading: { ...get().loading, isLoading: false } });
          return data;
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      clearAnalytics: () => {
        set({
          analytics: [],
          currentAnalytics: null,
        });
      },
    }),
    { name: 'analytics-store' }
  )
);

// Notifications Store
interface NotificationsStore {
  notifications: Notification[];
  unreadCount: number;
  loading: LoadingState;
  
  fetchNotifications: () => Promise<void>;
  markAsRead: (id: number) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  deleteNotification: (id: number) => Promise<void>;
  addNotification: (notification: Notification) => void;
  clearNotifications: () => void;
}

export const useNotificationsStore = create<NotificationsStore>()(
  devtools(
    (set, get) => ({
      notifications: [],
      unreadCount: 0,
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchNotifications: async () => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/notifications/');
          const unreadCount = response.results.filter((n: Notification) => !n.read).length;
          set({
            notifications: response.results,
            unreadCount,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      markAsRead: async (id) => {
        try {
          await apiService.patch(`/notifications/${id}/`, { read: true });
          set((state) => ({
            notifications: state.notifications.map((n) =>
              n.id === id ? { ...n, read: true } : n
            ),
            unreadCount: Math.max(0, state.unreadCount - 1),
          }));
        } catch (error: any) {
          console.error('Error marking notification as read:', error);
        }
      },

      markAllAsRead: async () => {
        try {
          await apiService.post('/notifications/mark-all-read/');
          set((state) => ({
            notifications: state.notifications.map((n) => ({ ...n, read: true })),
            unreadCount: 0,
          }));
        } catch (error: any) {
          console.error('Error marking all notifications as read:', error);
        }
      },

      deleteNotification: async (id) => {
        try {
          await apiService.delete(`/notifications/${id}/`);
          set((state) => ({
            notifications: state.notifications.filter((n) => n.id !== id),
            unreadCount: state.notifications.filter((n) => n.id !== id && !n.read).length,
          }));
        } catch (error: any) {
          console.error('Error deleting notification:', error);
        }
      },

      addNotification: (notification) => {
        set((state) => ({
          notifications: [notification, ...state.notifications],
          unreadCount: state.unreadCount + (notification.read ? 0 : 1),
        }));
      },

      clearNotifications: () => {
        set({
          notifications: [],
          unreadCount: 0,
        });
      },
    }),
    { name: 'notifications-store' }
  )
);

// Chat Store
interface ChatStore {
  rooms: ChatRoom[];
  currentRoom: ChatRoom | null;
  messages: ChatMessage[];
  typingUsers: User[];
  loading: LoadingState;
  
  fetchRooms: () => Promise<void>;
  joinRoom: (roomId: string) => Promise<void>;
  leaveRoom: (roomId: string) => Promise<void>;
  sendMessage: (roomId: string, content: string) => Promise<void>;
  fetchMessages: (roomId: string) => Promise<void>;
  clearChat: () => void;
}

export const useChatStore = create<ChatStore>()(
  devtools(
    (set, get) => ({
      rooms: [],
      currentRoom: null,
      messages: [],
      typingUsers: [],
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchRooms: async () => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get('/chat/rooms/');
          set({
            rooms: response.results,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      joinRoom: async (roomId) => {
        try {
          webSocketService.joinChatRoom(roomId);
          const room = get().rooms.find((r) => r.id === roomId);
          if (room) {
            set({ currentRoom: room });
            await get().fetchMessages(roomId);
          }
        } catch (error: any) {
          console.error('Error joining room:', error);
        }
      },

      leaveRoom: async (roomId) => {
        try {
          webSocketService.leaveChatRoom(roomId);
          set({ currentRoom: null, messages: [] });
        } catch (error: any) {
          console.error('Error leaving room:', error);
        }
      },

      sendMessage: async (roomId, content) => {
        try {
          webSocketService.sendMessage(roomId, { content });
        } catch (error: any) {
          console.error('Error sending message:', error);
        }
      },

      fetchMessages: async (roomId) => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const response = await apiService.get(`/chat/rooms/${roomId}/messages/`);
          set({
            messages: response.results,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      clearChat: () => {
        set({
          rooms: [],
          currentRoom: null,
          messages: [],
          typingUsers: [],
        });
      },
    }),
    { name: 'chat-store' }
  )
);

// Dashboard Store
interface DashboardStore {
  dashboardData: DashboardData | null;
  loading: LoadingState;
  
  fetchDashboardData: () => Promise<void>;
  refreshDashboard: () => Promise<void>;
  clearDashboard: () => void;
}

export const useDashboardStore = create<DashboardStore>()(
  devtools(
    (set, get) => ({
      dashboardData: null,
      loading: {
        isLoading: false,
        error: null,
        data: null,
      },

      fetchDashboardData: async () => {
        set({ loading: { ...get().loading, isLoading: true, error: null } });
        try {
          const data = await apiService.get('/dashboard/');
          set({
            dashboardData: data,
            loading: { ...get().loading, isLoading: false },
          });
        } catch (error: any) {
          set({
            loading: { ...get().loading, isLoading: false, error: error.message },
          });
        }
      },

      refreshDashboard: async () => {
        await get().fetchDashboardData();
      },

      clearDashboard: () => {
        set({
          dashboardData: null,
        });
      },
    }),
    { name: 'dashboard-store' }
  )
);