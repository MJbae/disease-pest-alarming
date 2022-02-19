from celery import shared_task

from forecasting.services.process_sms import send_sms


@shared_task
def send_sms_to_new(username, phone_number):
    message = f'{username}님 병해충예찰정보 문자서비스에 가입되었습니다.'
    send_sms(phone_number, message)
