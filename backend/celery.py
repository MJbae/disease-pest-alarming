from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.common")
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