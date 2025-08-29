import React, { useState, useEffect } from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, 
  X, 
  Home, 
  Users, 
  Brain, 
  BarChart3, 
  Camera, 
  Building2, 
  UserCheck, 
  BookOpen, 
  MessageCircle, 
  User, 
  Settings,
  Bell,
  LogOut
} from 'lucide-react';
import { useAuthStore } from '../../store';
import { useNotificationsStore } from '../../store';
import { webSocketService } from '../../services/websocket';
import { toast } from 'react-hot-toast';

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  
  const { user, logout } = useAuthStore();
  const { unreadCount, fetchNotifications } = useNotificationsStore();

  // Navigation items
  const navigationItems = [
    { name: 'Dashboard', icon: Home, path: '/dashboard' },
    { name: 'Students', icon: Users, path: '/students' },
    { name: 'AI Lessons', icon: Brain, path: '/ai-lessons' },
    { name: 'Analytics', icon: BarChart3, path: '/analytics' },
    { name: 'Monitoring', icon: Camera, path: '/monitoring' },
    { name: 'Families', icon: Building2, path: '/families' },
    { name: 'Staff', icon: UserCheck, path: '/staff' },
    { name: 'Lessons', icon: BookOpen, path: '/lessons' },
    { name: 'Chat', icon: MessageCircle, path: '/chat' },
  ];

  // Check if user has permission to access certain routes
  const hasPermission = (path: string) => {
    if (!user) return false;
    
    // Admin has access to everything
    if (user.role === 'admin') return true;
    
    // Role-based access control
    const rolePermissions: Record<string, string[]> = {
      student: ['/dashboard', '/ai-lessons', '/chat', '/profile', '/settings'],
      family: ['/dashboard', '/families', '/chat', '/profile', '/settings'],
      staff: ['/dashboard', '/students', '/ai-lessons', '/analytics', '/monitoring', '/lessons', '/chat', '/profile', '/settings'],
      ai_teacher: ['/dashboard', '/ai-lessons', '/analytics', '/chat', '/profile', '/settings'],
    };
    
    return rolePermissions[user.role]?.includes(path) || false;
  };

  // Filter navigation items based on user permissions
  const filteredNavigationItems = navigationItems.filter(item => hasPermission(item.path));

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  useEffect(() => {
    // Fetch notifications on mount
    fetchNotifications();
    
    // Set up WebSocket listeners for real-time notifications
    webSocketService.onNotification((notification) => {
      toast.success(notification.message);
      fetchNotifications(); // Refresh notifications
    });
    
    return () => {
      webSocketService.off('notification');
    };
  }, [fetchNotifications]);

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Logged out successfully');
      navigate('/login');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  const isActiveRoute = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <motion.div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-large transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        initial={{ x: -256 }}
        animate={{ x: sidebarOpen ? 0 : -256 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">AI School</h1>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* User Info */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-primary-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-xs text-gray-500 capitalize">
                  {user?.role?.replace('_', ' ')}
                </p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            {filteredNavigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <motion.button
                  key={item.name}
                  onClick={() => {
                    navigate(item.path);
                    if (isMobile) setSidebarOpen(false);
                  }}
                  className={`w-full flex items-center space-x-3 px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-200 ${
                    isActiveRoute(item.path)
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </motion.button>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="space-y-2">
              <button
                onClick={() => navigate('/profile')}
                className="w-full flex items-center space-x-3 px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 rounded-lg transition-colors duration-200"
              >
                <User className="w-5 h-5" />
                <span>Profile</span>
              </button>
              <button
                onClick={() => navigate('/settings')}
                className="w-full flex items-center space-x-3 px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 rounded-lg transition-colors duration-200"
              >
                <Settings className="w-5 h-5" />
                <span>Settings</span>
              </button>
              <button
                onClick={handleLogout}
                className="w-full flex items-center space-x-3 px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50 hover:text-red-700 rounded-lg transition-colors duration-200"
              >
                <LogOut className="w-5 h-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main content */}
      <div className="md:ml-64">
        {/* Top bar */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
              >
                <Menu className="w-5 h-5" />
              </button>
              <h2 className="text-lg font-semibold text-gray-900">
                {navigationItems.find(item => isActiveRoute(item.path))?.name || 'Dashboard'}
              </h2>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <button
                onClick={() => navigate('/notifications')}
                className="relative p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
              >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </button>

              {/* User menu */}
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-primary-600" />
                </div>
                <span className="hidden md:block text-sm font-medium text-gray-900">
                  {user?.first_name} {user?.last_name}
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
};

export default Layout;