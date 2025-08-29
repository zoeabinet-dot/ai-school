import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { HelmetProvider } from 'react-helmet-async';
import { QueryClient, QueryClientProvider } from 'react-query';

// Components
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import LoadingSpinner from './components/UI/LoadingSpinner';

// Pages
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import StudentsPage from './pages/Students/StudentsPage';
import StudentDetailPage from './pages/Students/StudentDetailPage';
import AILessonsPage from './pages/AILessons/AILessonsPage';
import AILessonDetailPage from './pages/AILessons/AILessonDetailPage';
import AnalyticsPage from './pages/Analytics/AnalyticsPage';
import MonitoringPage from './pages/Monitoring/MonitoringPage';
import FamiliesPage from './pages/Families/FamiliesPage';
import StaffPage from './pages/Staff/StaffPage';
import LessonsPage from './pages/Lessons/LessonsPage';
import ChatPage from './pages/Chat/ChatPage';
import ProfilePage from './pages/Profile/ProfilePage';
import SettingsPage from './pages/Settings/SettingsPage';
import NotFoundPage from './pages/NotFound/NotFoundPage';

// Stores
import { useAuthStore } from './store';

// Styles
import './styles/index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="App">
            <Routes>
              {/* Public Routes */}
              <Route 
                path="/login" 
                element={
                  isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />
                } 
              />
              <Route 
                path="/register" 
                element={
                  isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />
                } 
              />

              {/* Protected Routes */}
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<DashboardPage />} />
                <Route path="students" element={<StudentsPage />} />
                <Route path="students/:id" element={<StudentDetailPage />} />
                <Route path="ai-lessons" element={<AILessonsPage />} />
                <Route path="ai-lessons/:id" element={<AILessonDetailPage />} />
                <Route path="analytics" element={<AnalyticsPage />} />
                <Route path="monitoring" element={<MonitoringPage />} />
                <Route path="families" element={<FamiliesPage />} />
                <Route path="staff" element={<StaffPage />} />
                <Route path="lessons" element={<LessonsPage />} />
                <Route path="chat" element={<ChatPage />} />
                <Route path="profile" element={<ProfilePage />} />
                <Route path="settings" element={<SettingsPage />} />
              </Route>

              {/* 404 Route */}
              <Route path="*" element={<NotFoundPage />} />
            </Routes>

            {/* Toast Notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: '#22c55e',
                    secondary: '#fff',
                  },
                },
                error: {
                  duration: 5000,
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#fff',
                  },
                },
              }}
            />
          </div>
        </Router>
      </QueryClientProvider>
    </HelmetProvider>
  );
}

export default App;