from celery import shared_task

from forecasting.services.process_forecasting import process_latest_forecasting


@shared_task
def c_catch_latest_forecasting():
    process_latest_forecasting()
