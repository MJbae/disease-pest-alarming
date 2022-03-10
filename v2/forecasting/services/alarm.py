import os
import time
from typing import Set

import base64
import hashlib
import hmac
import requests

from forecasting.dtos import ForecastingDto, AffectedFarmDto


def send_alarms(farm_set: Set[AffectedFarmDto]) -> (str, int):
    """
    Send sms alarm message to affected farm owners

    Parameters:
        farm_set(Set[AffectedFarmDto]): contains affected farm's info

    Returns:
        (str, int): result of sending sms, times to success in sending sms
    """

    total_to_send = 0
    for farm in farm_set:
        message = _make_alarm_message(farm.info)
        result = _send_sms(to_number=farm.contact, content=message)

        if result['statusCode'] != "202":
            return "fail", total_to_send

        total_to_send += 1

    return "success", total_to_send


def _make_alarm_message(info):
    return f"{info.date}, {info.address_name}의 {info.crop_name}에서 {info.target_name} 피해 발생"


def _send_sms(to_number, content):
    access_key, secret_key = _get_key_vars()
    base_url, from_number, service_id = _get_reqeust_params()
    endpoint = f"/sms/v2/services/{service_id}/messages"
    full_uri = base_url + endpoint
    timestamp = str(int(time.time() * 1000))

    body = _make_body(content, from_number, to_number)

    signature = _make_signature(access_key, secret_key, 'POST', endpoint, timestamp)
    header = _make_header(access_key, signature, timestamp)

    res = requests.post(full_uri, json=body, headers=header)
    return res.json()


def _make_header(access_key, signature, timestamp):
    return {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature
    }


def _make_body(content, from_number, to_number):
    return {
        "type": "sms",
        "from": from_number,
        "content": content,
        "messages": [
            {
                "to": to_number,
                "subject": "병해충 예찰 서비스",
                "content": content
            }
        ]
    }


def _get_reqeust_params():
    base_url = os.environ.get("SENS_URL")
    service_id = os.environ.get("SENS_SERVICE_ID")
    from_number = os.environ.get("SENS_FROM_NUMBER")
    return base_url, from_number, service_id


def _get_key_vars():
    access_key = os.environ.get("SENS_ACCESS_KEY")
    secret_key = os.environ.get("SENS_SECRET_KEY")
    return access_key, secret_key


def _make_signature(access_key, secret_key, method, uri, timestamp):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    result = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return result
