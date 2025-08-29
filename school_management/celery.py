import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

app = Celery('school_management')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'generate-daily-reports': {
        'task': 'analytics.tasks.generate_daily_reports',
        'schedule': 86400.0,  # Run daily
    },
    'cleanup-old-sessions': {
        'task': 'accounts.tasks.cleanup_old_sessions',
        'schedule': 3600.0,  # Run hourly
    },
    'process-webcam-analytics': {
        'task': 'webcam_monitoring.tasks.process_analytics',
        'schedule': 300.0,  # Run every 5 minutes
    },
}

app.conf.timezone = 'Africa/Addis_Ababa'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')