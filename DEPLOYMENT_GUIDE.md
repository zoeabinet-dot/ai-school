# Alpha School AI - Deployment Guide

## 🚀 Quick Start with Docker

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space

### 1. Environment Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd school-management-system

# Copy environment file
cp .env.example .env

# Edit .env with your settings (especially OPENAI_API_KEY)
nano .env
```

### 2. Start the Application
```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f web
```

### 3. Access the Application
- **Web Interface**: http://localhost
- **API Documentation**: http://localhost/api/
- **Admin Panel**: http://localhost/admin/
  - Username: `admin`
  - Password: `admin123`

### 4. Demo Users
| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Student | student_demo | demo123 | Abebe Kebede - Grade 8 |
| Family | family_demo | demo123 | Almaz Kebede - Parent |
| Staff | staff_demo | demo123 | Dawit Mengistu - Teacher |
| Admin | admin_demo | demo123 | Meron Tadesse - Administrator |

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │     Django      │    │   PostgreSQL    │
│  (Reverse Proxy)│────│   (Web App)     │────│   (Database)    │
│     Port 80     │    │   Port 8000     │    │   Port 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌───────┴───────┐
                       │               │
                ┌─────────────┐ ┌─────────────┐
                │    Redis    │ │   Celery    │
                │ (Cache/MQ)  │ │  (Tasks)    │
                │  Port 6379  │ │             │
                └─────────────┘ └─────────────┘
```

## 🔧 Configuration

### Essential Environment Variables
```bash
# Database
DB_NAME=school_management
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=db
DB_PORT=5432

# AI Services (Required for AI features)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Security
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,your-domain.com

# Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## 📱 Feature Overview

### 🎓 Student Features
- **AI Teacher Chat**: Real-time conversation with intelligent tutor
- **Personalized Learning**: Adaptive learning paths based on performance
- **Progress Tracking**: Visual dashboards showing learning progress
- **Portfolio Management**: Upload and showcase projects and achievements
- **Webcam Monitoring**: Optional attention and engagement tracking

### 👨‍👩‍👧‍👦 Family Features
- **Child Monitoring**: Real-time progress and behavioral insights
- **Communication**: Direct messaging with staff and AI teacher
- **Reports**: Comprehensive academic and behavioral reports
- **Notifications**: Automated alerts and recommendations

### 👨‍🏫 Staff Features
- **Student Management**: Oversight of assigned students
- **Assignment Creation**: Create and grade assignments
- **Analytics Dashboard**: Performance trends and insights
- **AI Recommendations**: Data-driven teaching suggestions

### 👨‍💼 Admin Features
- **System Overview**: Complete platform analytics
- **User Management**: Manage all users and permissions
- **Performance Reports**: School-wide performance metrics
- **Configuration**: System settings and AI parameters

## 🤖 AI Integration

### OpenAI Integration
The system uses OpenAI's GPT models for:
- Conversational AI teacher
- Personalized learning recommendations
- Content generation
- Performance analysis

**Setup Instructions:**
1. Get API key from https://platform.openai.com/
2. Add to `.env` file: `OPENAI_API_KEY=your_key_here`
3. Restart the application

### Webcam AI Analysis
Computer vision features for:
- Attention level detection
- Emotion recognition
- Behavioral pattern analysis
- Engagement scoring

**Privacy Note:** All webcam features require explicit consent and can be disabled.

## 📊 Database Schema

### Core Models
- **User**: Base user model with role-based access
- **Student**: Student profiles with learning preferences
- **Family**: Parent/guardian accounts linked to students
- **Staff**: Teacher and assistant accounts
- **Administrator**: System admin accounts

### Learning Models
- **Subject**: Academic subjects (Math, Science, etc.)
- **LearningPath**: Personalized learning journeys
- **Lesson**: Individual learning units
- **Assignment**: Homework and projects
- **Quiz**: Assessments and tests

### Analytics Models
- **StudentPerformanceMetrics**: Academic performance tracking
- **EngagementMetrics**: Student engagement analysis
- **AttendanceRecord**: Attendance tracking
- **BehavioralObservation**: Behavioral pattern data

## 🔒 Security Features

### Authentication
- JWT-based authentication
- Role-based access control (RBAC)
- Password encryption
- Session management

### Data Protection
- HTTPS enforcement (production)
- Data encryption at rest
- Input validation and sanitization
- CSRF protection
- XSS prevention

### Privacy Compliance
- Webcam consent management
- Data retention policies
- Audit logging
- GDPR-compliant data handling

## 🚀 Production Deployment

### Cloud Deployment Options

#### AWS Deployment
```bash
# Use AWS ECS with RDS and ElastiCache
# Docker images can be pushed to ECR
# Use Application Load Balancer for scaling
```

#### Google Cloud Platform
```bash
# Use Cloud Run with Cloud SQL and Memorystore
# Container images in Container Registry
# Use Cloud Load Balancing
```

#### DigitalOcean
```bash
# Use App Platform or Droplets
# Managed PostgreSQL and Redis
# Use Load Balancer for high availability
```

### SSL/HTTPS Setup
1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update nginx.conf with SSL configuration
3. Set `SECURE_SSL_REDIRECT=True` in environment
4. Update ALLOWED_HOSTS with your domain

### Monitoring Setup
```bash
# Add monitoring services
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Services include:
# - Prometheus (metrics)
# - Grafana (dashboards)
# - ELK Stack (logging)
```

## 🛠️ Development Setup

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py create_demo_data
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Development Tools
```bash
# Code formatting
black .
isort .

# Linting
flake8 .

# Testing
python manage.py test

# Database migrations
python manage.py makemigrations
python manage.py migrate
```

## 📈 Performance Optimization

### Database Optimization
- Use PostgreSQL connection pooling
- Implement database indexing
- Use select_related() and prefetch_related()
- Regular database maintenance

### Caching Strategy
- Redis for session caching
- API response caching
- Static file caching with CDN
- Database query caching

### Scaling Considerations
- Horizontal scaling with load balancers
- Database read replicas
- Celery worker scaling
- CDN for static assets

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database service
docker-compose logs db

# Verify connection
docker-compose exec web python manage.py dbshell
```

#### AI Features Not Working
```bash
# Check OpenAI API key
docker-compose exec web python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Test API connection
docker-compose exec web python manage.py shell
>>> import openai
>>> openai.api_key = "your_key"
>>> openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "test"}])
```

#### Permission Errors
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### Log Analysis
```bash
# View application logs
docker-compose logs -f web

# View database logs
docker-compose logs -f db

# View all services
docker-compose logs -f
```

## 📞 Support

### Getting Help
- Check logs for error messages
- Review environment configuration
- Verify all services are running
- Check network connectivity

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

### Contact
- GitHub Issues: For bug reports and feature requests
- Documentation: Check README.md for additional details
- Community: Join our Discord/Slack for discussions

---

**🎉 Congratulations!** 
You now have a fully functional AI-powered school management system running. The platform is ready to revolutionize education in Addis Ababa with its advanced AI features, comprehensive analytics, and user-friendly interfaces.

**Next Steps:**
1. Customize the system for your specific needs
2. Train staff on using the platform
3. Set up monitoring and backups
4. Scale according to your user base

*Built with ❤️ for Ethiopian Education*