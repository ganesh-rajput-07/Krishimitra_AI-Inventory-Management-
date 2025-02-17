import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krishimitra_ai.settings')

app = Celery('krishimitra_ai')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

from celery.schedules import crontab
from celery import Celery

app = Celery("krishimitra_ai")

app.conf.beat_schedule = {
    "check_spoilage_daily": {
        "task": "inventory.tasks.check_spoilage",
        "schedule": crontab(hour=9, minute=0),  # Runs daily at 9 AM
    },
}
