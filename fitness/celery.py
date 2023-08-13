# import os
# from celery import Celery
# from django.conf import settings
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')
#
# app = Celery('fitness')
#
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')

app = Celery('fitness')

try:
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
except Exception as e:
    print(f"\n\n\n546275482746568724568 An error occurred: {e}")
    raise

