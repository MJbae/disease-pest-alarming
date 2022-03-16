import os

from celery import Celery
from celery.schedules import crontab

from config.settings.common import DJANGO_ENV, INSTALLED_APPS

if DJANGO_ENV == "dev":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
if DJANGO_ENV == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

app = Celery("config")

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(INSTALLED_APPS)

app.conf.beat_schedule = {
    "process_the_latest_forecasting": {
        "task": "forecasting.tasks.c_process_the_latest_forecasting",
        "schedule": crontab(),
        "args": (),
    },
}
