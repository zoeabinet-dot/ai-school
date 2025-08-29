# Alpha School AI Management System

A comprehensive Django-based school management and AI-learning system inspired by Alpha School's AI-driven education model, specifically adapted for Addis Ababa.

## 🌟 Features

### Core Vision
Replace traditional schooling structures with an AI-first model where students interact with AI-driven lessons, analytics, and personalized feedback while staff, families, and stakeholders monitor progress, engagement, and personal development.

### User Roles
- **Students**: Personalized AI lessons, progress tracking, project portfolio, AI teacher conversations
- **Families/Guardians**: Progress monitoring, behavioral reports, AI recommendations, messaging
- **Staff/Teachers**: Student oversight, AI recommendations, attendance tracking, lesson plan adjustments
- **Administrators**: Full analytics, performance reports, staff/student management, system oversight
- **AI Teacher**: Conversational AI, personalized recommendations, live monitoring, automated reports

### Key Features
- 🤖 **AI-Powered Teaching**: Personalized lessons with real-time conversation
- 📊 **Advanced Analytics**: Student growth trajectories, engagement metrics, behavioral analysis
- 📹 **Smart Monitoring**: AI-powered webcam analysis for attention and behavior tracking
- 🎯 **Role-Based Dashboards**: Customized interfaces for each user type
- 🔒 **Enterprise Security**: JWT authentication, role-based permissions, data encryption
- 🌍 **Localized for Ethiopia**: Designed for Addis Ababa educational context

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.13+ (for local development)
- PostgreSQL (for production)
- Redis (for caching and task queue)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd school-management-system
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Web Interface: http://localhost
   - API Documentation: http://localhost/api/
   - Admin Panel: http://localhost/admin/

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py create_demo_data
   python manage.py createsuperuser
   ```

4. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🏗️ Architecture

### Backend
- **Django 5.0.1**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker
- **Celery**: Background task processing
- **JWT**: Authentication system

### AI Services
- **OpenAI GPT**: Conversational AI teacher
- **Whisper**: Speech recognition
- **gTTS**: Text-to-speech
- **OpenCV**: Computer vision for webcam analysis

### Frontend
- **HTML/CSS**: Modern responsive design
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Data visualization
- **Vanilla JavaScript**: Interactive features

### Infrastructure
- **Docker**: Containerization
- **Nginx**: Reverse proxy and static file serving
- **Gunicorn**: WSGI server

## 📱 User Interfaces

### Student Dashboard
- Learning progress tracking
- AI teacher chat interface
- Assignment submissions
- Portfolio management
- Performance analytics

### Family Dashboard
- Child progress monitoring
- Behavioral reports
- Communication with staff
- AI recommendations

### Staff Dashboard
- Student management
- Assignment creation
- Progress analytics
- AI-generated insights

### Admin Dashboard
- System-wide analytics
- User management
- Performance reports
- Configuration settings

## 🤖 AI Features

### AI Teacher
- Natural language conversations
- Personalized learning recommendations
- Context-aware responses
- Multi-language support (English/Amharic)

### Webcam Monitoring
- Attention level tracking
- Emotion analysis
- Behavioral pattern recognition
- Privacy-compliant recording

### Analytics Engine
- Learning pattern analysis
- Performance prediction
- Engagement optimization
- Automated reporting

## 🔧 Configuration

### Environment Variables
```bash
# Database
DB_NAME=school_management
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# AI Services
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo

# Security
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,your-domain.com

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Demo Users
The system comes with pre-configured demo users:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Student | student_demo | demo123 | Sample student account |
| Family | family_demo | demo123 | Parent/guardian account |
| Staff | staff_demo | demo123 | Teacher assistant account |
| Admin | admin_demo | demo123 | Administrator account |

## 📊 API Documentation

### Authentication
```bash
# Login
POST /api/auth/login/
{
  "username": "student_demo",
  "password": "demo123"
}

# Response
{
  "access": "jwt_token",
  "refresh": "refresh_token",
  "user": {
    "id": 1,
    "username": "student_demo",
    "role": "student"
  }
}
```

### Key Endpoints
- `/api/auth/` - Authentication endpoints
- `/api/learning/` - Learning management
- `/api/analytics/` - Analytics and reports
- `/api/ai-teacher/` - AI teacher interactions
- `/api/webcam/` - Webcam monitoring

## 🛡️ Security Features

- JWT-based authentication
- Role-based access control
- Data encryption at rest
- HTTPS enforcement
- Rate limiting
- Input validation
- CSRF protection
- XSS prevention

## 🌍 Localization

The system is designed for the Ethiopian educational context:
- Amharic language support
- Ethiopian calendar integration
- Local curriculum alignment
- Cultural context awareness
- Time zone configuration (Africa/Addis_Ababa)

## 📈 Monitoring & Analytics

### System Metrics
- User engagement tracking
- Performance monitoring
- Error logging
- Resource utilization

### Educational Analytics
- Learning progress tracking
- Attention span analysis
- Behavioral pattern recognition
- Performance prediction

## 🚀 Deployment

### Production Deployment
1. Set up SSL certificates
2. Configure environment variables
3. Set up monitoring (optional)
4. Deploy using Docker Compose

### Cloud Deployment
The system is ready for deployment on:
- AWS (EC2, RDS, ElastiCache)
- Google Cloud Platform
- Microsoft Azure
- DigitalOcean

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔮 Future Roadmap

- Mobile application (React Native)
- Advanced AI features (GPT-4, custom models)
- Blockchain-based certificates
- VR/AR learning experiences
- Advanced biometric monitoring
- Machine learning model optimization

---

**Built with ❤️ for Ethiopian Education**

*Empowering the next generation through AI-driven learning*