from celery import shared_task

from forecasting.services.process_forecasting import catch_latest_forecasting


@shared_task
def c_catch_latest_forecasting():
    catch_latest_forecasting()
