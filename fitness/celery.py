import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')

app = Celery('fitness')

app.conf.timezone = 'Europe/Moscow'

try:
    app.config_from_object('django.conf:settings', namespace="CELERY")
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    app.conf.beat_schedule = {
        'add-every-60-min': {
            'task': 'subscription.tasks.check_time_subscriptions_finish',
            'schedule': 60.0 * 60,
        },
    }
except Exception as e:
    print(f"\n\n\n546275482746568724568 An error occurred: {e}")
    raise
