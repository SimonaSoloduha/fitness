# from .celery import app as celery_app

# your_project_name/__init__.py
from __future__ import absolute_import, unicode_literals

# Загружаем celery app при старте Django
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except Exception as e:
    import logging
    logging.error(f"Failed to load Celery app: {e}")
