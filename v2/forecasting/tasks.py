from celery import shared_task
import logging

from forecasting.services.forecasting import collect_the_latest_forecasting
from forecasting.services.farm import find_affected_farms
from forecasting.services.alarm import send_alarms

logger = logging.getLogger('celery')


@shared_task
def c_process_the_latest_forecasting():
    forecasting_set = collect_the_latest_forecasting()
    farm_set = find_affected_farms(forecasting_set)
    result, success_to_send = send_alarms(farm_set)
    logger.info(msg=f'result: {result}, success_to_send: {success_to_send}')
