#!/bin/bash

# AI School Management System Deployment Script
# This script automates the deployment process for both development and production environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai_school_management"
ENVIRONMENT=${1:-development}  # development, staging, production
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        create_env_file
    fi
    
    print_success "Prerequisites check completed"
}

# Function to create .env file from template
create_env_file() {
    cat > .env << EOF
# AI School Management System Environment Configuration

# Django Settings
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DATABASE_URL=postgresql://ai_school_user:ai_school_password@db:5432/ai_school_db
POSTGRES_DB=ai_school_db
POSTGRES_USER=ai_school_user
POSTGRES_PASSWORD=ai_school_password

# AI Services
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Security
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# File Upload
MAX_UPLOAD_SIZE=52428800
FILE_UPLOAD_MAX_MEMORY_SIZE=52428800
EOF

    print_warning "Please update the .env file with your actual API keys and configuration values"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p media staticfiles logs nginx/conf.d ssl monitoring/grafana ai_models
    
    print_success "Directories created"
}

# Function to create Nginx configuration
create_nginx_config() {
    print_status "Creating Nginx configuration..."
    
    # Main nginx.conf
    cat > nginx/nginx.conf << EOF
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                    '\$status \$body_bytes_sent "\$http_referer" '
                    '"\$http_user_agent" "\$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone \$binary_remote_addr zone=login:10m rate=5r/m;
    
    include /etc/nginx/conf.d/*.conf;
}
EOF

    # Default site configuration
    cat > nginx/conf.d/default.conf << EOF
server {
    listen 80;
    server_name localhost;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # API endpoints with rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Admin interface
    location /admin/ {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
    
    # Main application
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

    print_success "Nginx configuration created"
}

# Function to create monitoring configuration
create_monitoring_config() {
    print_status "Creating monitoring configuration..."
    
    # Prometheus configuration
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'django'
    static_configs:
      - targets: ['web:8000']
    metrics_path: '/metrics/'
    scrape_interval: 30s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']
    scrape_interval: 30s
EOF

    print_success "Monitoring configuration created"
}

# Function to build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Build images
    docker-compose build
    
    # Start services based on environment
    case $ENVIRONMENT in
        "development")
            print_status "Starting development environment..."
            docker-compose --profile dev up -d
            ;;
        "staging")
            print_status "Starting staging environment..."
            docker-compose up -d web db redis nginx
            ;;
        "production")
            print_status "Starting production environment..."
            docker-compose up -d
            ;;
        *)
            print_error "Invalid environment: $ENVIRONMENT"
            print_status "Available environments: development, staging, production"
            exit 1
            ;;
    esac
    
    print_success "Services started successfully"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for database
    print_status "Waiting for database..."
    until docker-compose exec -T db pg_isready -U ai_school_user -d ai_school_db; do
        sleep 2
    done
    
    # Wait for web service
    print_status "Waiting for web service..."
    until curl -f http://localhost:8000/health/ > /dev/null 2>&1; do
        sleep 5
    done
    
    print_success "All services are ready"
}

# Function to run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    docker-compose exec web python manage.py migrate
    
    print_success "Database migrations completed"
}

# Function to create superuser
create_superuser() {
    print_status "Creating superuser..."
    
    read -p "Do you want to create a superuser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose exec web python manage.py createsuperuser
    fi
}

# Function to collect static files
collect_static() {
    print_status "Collecting static files..."
    
    docker-compose exec web python manage.py collectstatic --noinput
    
    print_success "Static files collected"
}

# Function to show service status
show_status() {
    print_status "Service status:"
    docker-compose ps
    
    echo
    print_status "Service URLs:"
    echo "Main Application: http://localhost:8000"
    echo "Admin Interface: http://localhost:8000/admin/"
    echo "API Documentation: http://localhost:8000/api/v1/"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "Nginx: http://localhost:80"
        echo "Grafana: http://localhost:3000 (admin/admin)"
        echo "Prometheus: http://localhost:9090"
        echo "Flower (Celery): http://localhost:5555"
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing logs for $ENVIRONMENT environment..."
    docker-compose logs -f
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    
    read -p "This will remove all containers, volumes, and images. Are you sure? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v --rmi all
        docker system prune -f
        print_success "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Main deployment function
main() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}AI School Management System${NC}"
    echo -e "${BLUE}Deployment Script${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
    
    print_status "Environment: $ENVIRONMENT"
    print_status "Project: $PROJECT_NAME"
    echo
    
    case $1 in
        "deploy")
            check_prerequisites
            create_directories
            create_nginx_config
            create_monitoring_config
            deploy_services
            wait_for_services
            run_migrations
            collect_static
            create_superuser
            show_status
            ;;
        "start")
            deploy_services
            wait_for_services
            show_status
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            deploy_services
            wait_for_services
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"--help"|"-h")
            echo "Usage: $0 [command] [environment]"
            echo ""
            echo "Commands:"
            echo "  deploy     Full deployment (default)"
            echo "  start      Start existing services"
            echo "  stop       Stop services"
            echo "  restart    Restart services"
            echo "  status     Show service status"
            echo "  logs       Show service logs"
            echo "  cleanup    Remove all containers and volumes"
            echo "  help       Show this help message"
            echo ""
            echo "Environments:"
            echo "  development (default)"
            echo "  staging"
            echo "  production"
            echo ""
            echo "Examples:"
            echo "  $0 deploy production"
            echo "  $0 start development"
            echo "  $0 status"
            ;;
        *)
            print_error "Invalid command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Check if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi