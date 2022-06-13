import os
from celery import Celery

# Set the default Django settings module for the Celery program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_shop.settings')

app = Celery('my_shop')

# Load any custom configuration from project settings.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
