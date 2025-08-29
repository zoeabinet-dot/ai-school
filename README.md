# AI School Management System

A comprehensive, AI-powered school management and learning platform inspired by Alpha School's AI-driven education model, specifically adapted for Addis Ababa and similar educational environments.

## 🌟 Core Vision

This application replaces traditional schooling structures with an AI-first model where students interact with AI-driven lessons, analytics, and personalized feedback while staff, families, and stakeholders can monitor progress, engagement, and personal development.

## 🚀 Key Features

### 🤖 AI-Powered Learning
- **Personalized AI Lessons**: Text, audio, video, and interactive chat-based learning
- **Adaptive Curriculum**: AI adjusts lessons based on student performance and learning style
- **Natural Language Processing**: Conversational AI teacher with speech recognition and synthesis
- **Behavioral Analysis**: Real-time webcam monitoring for engagement and attention tracking

### 👥 Multi-Role System
- **Students**: AI lessons, progress tracking, project portfolios
- **Families/Guardians**: Progress monitoring, notifications, communication
- **Staff/Teachers**: Student oversight, AI recommendations, attendance tracking
- **Administrators**: Full system access, analytics, performance reports
- **AI Teacher**: Virtual role for automated teaching and guidance

### 📊 Advanced Analytics
- **Learning Analytics**: Comprehensive student performance tracking
- **Engagement Metrics**: Time spent, attention scores, activity logs
- **Scientific Dashboards**: Graphs, charts, and trend analysis
- **AI-Driven Insights**: Behavioral analysis and learning recommendations

### 🔒 Security & Privacy
- **JWT Authentication**: Secure, token-based authentication system
- **Role-Based Access Control**: Fine-grained permissions for different user types
- **Privacy Compliance**: GDPR-compliant data handling and consent management
- **Encrypted Storage**: Secure handling of sensitive student data

## 🏗️ Technical Architecture

### Backend Stack
- **Django 5.0+**: Robust Python web framework
- **Django REST Framework**: Powerful API development
- **PostgreSQL**: Scalable, analytics-ready database
- **JWT Authentication**: Secure token-based authentication

### AI & Machine Learning
- **OpenAI GPT**: Advanced language model integration
- **Whisper**: Speech-to-text processing
- **gTTS**: Text-to-speech synthesis
- **OpenCV**: Computer vision for behavioral analysis
- **TensorFlow**: Deep learning capabilities

### Frontend & UI
- **Modern HTML/CSS**: Clean, responsive design
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js/Plotly**: Interactive data visualizations
- **Progressive Web App**: Mobile-friendly interface

### Deployment & Scalability
- **Docker**: Containerized deployment
- **Kubernetes**: Scalable orchestration (optional)
- **Nginx**: Reverse proxy and load balancing
- **Cloud-Ready**: AWS/GCP/Azure deployment support

## 📁 Project Structure

```
ai_school_management/
├── accounts/                 # User management and authentication
├── students/                 # Student profiles and academic records
├── families/                 # Family/guardian management
├── staff/                    # Staff and teacher management
├── ai_teacher/              # AI lesson and conversation system
├── analytics/               # Learning analytics and reporting
├── lessons/                 # Lesson management system
├── monitoring/              # Webcam monitoring and behavioral analysis
├── ai_school_management/    # Main project configuration
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── media/                   # User uploads and media files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Node.js 16+ (for frontend build tools)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai_school_management
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_school_db

# AI Services
OPENAI_API_KEY=your-openai-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### 5. Set Up Database
```bash
# Create PostgreSQL database
createdb ai_school_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🔧 Configuration

### Database Configuration
The system supports both PostgreSQL (production) and SQLite (development):

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_school_db',
        'USER': 'ai_school_user',
        'PASSWORD': 'ai_school_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# For development with SQLite
if os.environ.get('USE_SQLITE', 'false').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### AI Service Configuration
Configure AI services in your environment variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4

# Speech Services
ELEVENLABS_API_KEY=your-api-key
WHISPER_MODEL=base

# Computer Vision
OPENCV_ENABLED=True
BEHAVIOR_ANALYSIS_ENABLED=True
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/token/` - Obtain JWT token
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/logout/` - User logout

### AI Teacher Endpoints
- `GET /api/v1/ai-teacher/lessons/` - List AI lessons
- `POST /api/v1/ai-teacher/conversations/create/` - Create conversation
- `POST /api/v1/ai-teacher/chat/` - General AI chat
- `POST /api/v1/ai-teacher/speech-to-text/` - Speech recognition
- `POST /api/v1/ai-teacher/text-to-speech/` - Text synthesis

### Student Management
- `GET /api/v1/students/` - List students
- `GET /api/v1/students/<id>/` - Student details
- `POST /api/v1/students/` - Create student
- `PUT /api/v1/students/<id>/` - Update student

### Analytics & Reporting
- `GET /api/v1/analytics/learning/` - Learning analytics
- `GET /api/v1/analytics/performance/` - Performance metrics
- `GET /api/v1/analytics/engagement/` - Engagement analytics

## 🎯 Usage Examples

### Creating an AI Lesson
```python
from ai_teacher.models import AILesson

lesson = AILesson.objects.create(
    title="Introduction to Mathematics",
    subject="Mathematics",
    grade_level="1",
    difficulty_level="beginner",
    lesson_type="interactive",
    content={
        "sections": [
            {"type": "introduction", "content": "Welcome to math!"},
            {"type": "practice", "content": "Let's count together"}
        ]
    },
    learning_objectives=["Count to 10", "Recognize numbers"],
    estimated_duration=30
)
```

### Starting an AI Conversation
```python
from ai_teacher.models import AIConversation

conversation = AIConversation.objects.create(
    student=student_user,
    conversation_id=str(uuid.uuid4()),
    ai_model="gpt-4",
    ai_personality="helpful_teacher"
)
```

### Analyzing Student Behavior
```python
from monitoring.models import AIBehavioralAnalysis

analysis = AIBehavioralAnalysis.objects.create(
    student=student_user,
    session=learning_session,
    attention_score=85.5,
    engagement_level="high",
    focus_quality="focused",
    emotional_state="focused"
)
```

## 🚀 Deployment

### Production Deployment
1. **Set up production server** (Ubuntu 20.04+ recommended)
2. **Install system dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip postgresql nginx
   ```
3. **Configure PostgreSQL**:
   ```bash
   sudo -u postgres createdb ai_school_db
   sudo -u postgres createuser ai_school_user
   ```
4. **Set up environment variables**:
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   ```
5. **Run migrations**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```
6. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/staticfiles/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment
```bash
# Build Docker image
docker build -t ai-school-management .

# Run with Docker Compose
docker-compose up -d
```

## 🔒 Security Considerations

- **JWT Token Security**: Tokens expire automatically and can be revoked
- **Role-Based Access**: Users can only access data appropriate to their role
- **Data Encryption**: Sensitive data is encrypted at rest and in transit
- **Privacy Compliance**: GDPR-compliant data handling and consent management
- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Protection**: Django ORM provides built-in protection

## 📊 Monitoring & Analytics

### Built-in Analytics
- **Student Performance Tracking**: Grades, attendance, engagement
- **Learning Analytics**: Time spent, progress rates, skill development
- **Behavioral Analysis**: Attention scores, engagement patterns
- **AI Effectiveness**: Response quality, user satisfaction

### Custom Reports
- **Academic Reports**: Subject performance, grade trends
- **Behavioral Reports**: Engagement patterns, attention analysis
- **AI Insights**: Learning recommendations, intervention suggestions
- **Export Options**: PDF, Excel, CSV formats

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)

### Community
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discord Community](https://discord.gg/your-community)
- [Email Support](mailto:support@your-domain.com)

### Troubleshooting
Common issues and solutions:
- **Database Connection**: Check PostgreSQL service and credentials
- **AI Services**: Verify API keys and service availability
- **File Uploads**: Ensure media directory permissions
- **Email Sending**: Check SMTP configuration

## 🌟 Acknowledgments

- **Alpha School**: Inspiration for AI-driven education model
- **OpenAI**: Advanced language model capabilities
- **Django Community**: Robust web framework
- **Open Source Contributors**: Various libraries and tools

## 🔮 Future Roadmap

### Phase 2: Advanced AI Features
- **Multi-language Support**: Amharic, Oromo, and other local languages
- **Advanced Computer Vision**: More sophisticated behavioral analysis
- **Predictive Analytics**: AI-powered learning outcome predictions
- **Natural Language Understanding**: Better conversation context

### Phase 3: Integration & Expansion
- **LMS Integration**: Moodle, Canvas compatibility
- **Mobile Applications**: Native iOS and Android apps
- **Offline Capabilities**: Local AI models for low-connectivity areas
- **Advanced Reporting**: Custom dashboard builder

### Phase 4: Enterprise Features
- **Multi-school Management**: District and regional administration
- **Advanced Analytics**: Machine learning insights and predictions
- **API Ecosystem**: Third-party integrations and plugins
- **Global Deployment**: Multi-region, multi-currency support

---

**Built with ❤️ for the future of education in Addis Ababa and beyond.**