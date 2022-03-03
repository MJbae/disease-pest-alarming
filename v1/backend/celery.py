import os

from celery import Celery
from celery.schedules import crontab

from backend.settings.common import DJANGO_ENV

if DJANGO_ENV == "dev":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
if DJANGO_ENV == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")

app = Celery("backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "catch_latest_forecasting": {
        "task": "forecasting.tasks.c_catch_latest_forecasting",
        "schedule": crontab(minute='30'),
        "args": (),
    },
}
