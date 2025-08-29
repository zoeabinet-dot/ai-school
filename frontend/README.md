# Addis Ababa AI School Management System - Frontend

A modern, responsive React frontend for the Addis Ababa AI School Management System, featuring advanced AI/ML integration, real-time communication, and comprehensive user management.

## 🚀 Features

### ✨ Modern UI/UX
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Smooth Animations**: Framer Motion for delightful interactions
- **Dark/Light Mode**: Theme support with system preference detection
- **Accessibility**: WCAG 2.1 compliant with screen reader support

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Granular permissions for different user roles
- **Automatic Token Refresh**: Seamless session management
- **Biometric Authentication**: Face ID and fingerprint support (mobile)

### 📊 Real-Time Features
- **WebSocket Integration**: Real-time updates and notifications
- **Live Chat**: Instant messaging with typing indicators
- **Live Monitoring**: Real-time student behavior tracking
- **Performance Updates**: Live analytics and progress tracking

### 🤖 AI/ML Integration
- **AI-Powered Lessons**: Dynamic content generation
- **Emotion Recognition**: Multi-modal emotion detection
- **Predictive Analytics**: ML-based performance forecasting
- **Adaptive Learning**: Personalized content recommendations

### 📱 Mobile Optimization
- **Progressive Web App**: Offline functionality and app-like experience
- **Touch Gestures**: Swipe, pinch, and tap interactions
- **Mobile-First Design**: Optimized for all screen sizes
- **Performance**: Optimized loading and smooth animations

## 🛠️ Technology Stack

### Core Framework
- **React 18**: Latest React features with concurrent rendering
- **TypeScript**: Type-safe development with strict type checking
- **React Router 6**: Modern routing with nested routes
- **React Query**: Server state management and caching

### UI & Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Advanced animations and transitions
- **Lucide React**: Beautiful, customizable icons
- **React Hook Form**: Performant forms with validation

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state and caching
- **Local Storage**: Persistent client-side storage

### Real-Time Communication
- **Socket.IO**: WebSocket client for real-time features
- **WebRTC**: Peer-to-peer communication
- **Server-Sent Events**: Real-time notifications

### Performance & Optimization
- **React.memo**: Component memoization
- **Code Splitting**: Dynamic imports for better performance
- **Lazy Loading**: On-demand component loading
- **Service Workers**: Offline functionality and caching

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Auth/           # Authentication components
│   ├── Layout/         # Layout and navigation
│   └── UI/             # Basic UI components
├── pages/              # Page components
│   ├── Auth/           # Login, register pages
│   ├── Dashboard/      # Main dashboard
│   ├── Students/       # Student management
│   ├── AILessons/      # AI-powered lessons
│   ├── Analytics/      # Data analytics
│   ├── Monitoring/     # Student monitoring
│   ├── Families/       # Family management
│   ├── Staff/          # Staff management
│   ├── Lessons/        # Traditional lessons
│   ├── Chat/           # Real-time chat
│   ├── Profile/        # User profile
│   └── Settings/       # Application settings
├── services/           # API and external services
│   ├── api.ts          # Main API service
│   └── websocket.ts    # WebSocket service
├── store/              # State management
│   └── index.ts        # Zustand stores
├── hooks/              # Custom React hooks
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
├── assets/             # Static assets
└── styles/             # Global styles
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running (Django server)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000/api
   REACT_APP_WS_URL=ws://localhost:8000/ws
   REACT_APP_ENVIRONMENT=development
   ```

4. **Start Development Server**
   ```bash
   npm start
   # or
   yarn start
   ```

5. **Open in Browser**
   Navigate to `http://localhost:3000`

## 🔧 Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm lint` - Run ESLint
- `npm lint:fix` - Fix ESLint errors
- `npm format` - Format code with Prettier
- `npm type-check` - Run TypeScript type checking

### Code Quality

- **ESLint**: Code linting with React and TypeScript rules
- **Prettier**: Code formatting
- **TypeScript**: Strict type checking
- **Husky**: Git hooks for pre-commit checks

### Testing

- **Jest**: Unit testing framework
- **React Testing Library**: Component testing
- **MSW**: API mocking for tests

## 📱 Responsive Design

The application is built with a mobile-first approach:

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Breakpoints
```css
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Secondary**: Gray (#64748b)
- **Success**: Green (#22c55e)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

### Typography
- **Font Family**: Inter (sans-serif)
- **Monospace**: JetBrains Mono
- **Font Weights**: 300, 400, 500, 600, 700

### Components
- **Buttons**: Primary, secondary, success, warning, danger variants
- **Cards**: Elevated cards with shadows
- **Forms**: Consistent form styling with validation
- **Modals**: Overlay modals with animations
- **Navigation**: Responsive sidebar and top navigation

## 🔐 Authentication Flow

1. **Login**: User enters credentials and role
2. **Token Storage**: JWT tokens stored in localStorage
3. **Auto Refresh**: Automatic token refresh before expiration
4. **Route Protection**: Protected routes check authentication
5. **Role-Based Access**: Navigation filtered by user permissions

## 📊 Real-Time Features

### WebSocket Events
- `chat_message` - New chat messages
- `behavior_alert` - Student behavior alerts
- `performance_update` - Performance updates
- `notification` - System notifications
- `ai_model_update` - AI model updates

### Real-Time Updates
- Live student activity monitoring
- Real-time chat with typing indicators
- Instant notifications and alerts
- Live performance tracking
- Real-time AI model status

## 🤖 AI/ML Integration

### AI Features
- **Content Generation**: AI-powered lesson creation
- **Performance Prediction**: ML-based forecasting
- **Emotion Recognition**: Multi-modal emotion detection
- **Adaptive Learning**: Personalized content recommendations
- **Risk Assessment**: Early warning systems

### ML Models
- **Performance Predictor**: Student performance forecasting
- **Emotion Recognizer**: Facial and voice emotion detection
- **Content Generator**: Educational content generation
- **Risk Assessor**: Student risk assessment

## 📈 Performance Optimization

### Code Splitting
- Route-based code splitting
- Component lazy loading
- Dynamic imports for heavy components

### Caching
- React Query for API caching
- Service Worker for offline caching
- Local storage for user preferences

### Bundle Optimization
- Tree shaking for unused code
- Image optimization and lazy loading
- Gzip compression for assets

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Environment Variables
```env
REACT_APP_API_URL=https://api.addisababa-ai-school.com
REACT_APP_WS_URL=wss://api.addisababa-ai-school.com/ws
REACT_APP_ENVIRONMENT=production
```

### Deployment Platforms
- **Vercel**: Recommended for React apps
- **Netlify**: Static site hosting
- **AWS S3**: Static website hosting
- **Docker**: Containerized deployment

## 🔧 Configuration

### API Configuration
```typescript
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};
```

### WebSocket Configuration
```typescript
const WS_CONFIG = {
  url: process.env.REACT_APP_WS_URL,
  options: {
    transports: ['websocket', 'polling'],
    autoConnect: false,
    reconnection: true,
  },
};
```

## 📚 API Integration

### Authentication Endpoints
- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `POST /auth/refresh/` - Token refresh
- `POST /auth/logout/` - User logout

### Student Management
- `GET /students/` - List students
- `POST /students/` - Create student
- `GET /students/{id}/` - Get student details
- `PUT /students/{id}/` - Update student
- `DELETE /students/{id}/` - Delete student

### AI Lessons
- `GET /ai-teacher/lessons/` - List AI lessons
- `POST /ai-teacher/lessons/` - Create AI lesson
- `POST /ai-teacher/generate-lesson/` - Generate AI lesson

### Analytics
- `GET /analytics/learning-analytics/` - Learning analytics
- `POST /analytics/generate-report/` - Generate reports
- `GET /analytics/export/` - Export data

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Check if backend server is running
   - Verify API URL in environment variables
   - Check CORS configuration

2. **WebSocket Connection Issues**
   - Ensure WebSocket server is running
   - Check WebSocket URL configuration
   - Verify authentication tokens

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript errors
   - Verify all dependencies are installed

### Debug Mode
```bash
REACT_APP_DEBUG=true npm start
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow TypeScript best practices
- Use functional components with hooks
- Implement proper error handling
- Add comprehensive comments

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for Addis Ababa AI School Management System**