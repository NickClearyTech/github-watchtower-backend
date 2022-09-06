import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("watchtower_service", include=["tasks.data_collection_tasks"])

app.config_from_object("django.conf:settings")
