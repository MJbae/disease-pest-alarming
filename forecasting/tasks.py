from celery import shared_task

from forecasting.services.forecasting import catch_latest_forecasting


@shared_task
def c_catch_latest_forecasting():
    catch_latest_forecasting()
