import base64
import hashlib
import hmac
import os
import time

import requests

from accounts.models import User
from forecasting.models import Farm, ProducingCrop


def send_forecasting_to_owners(latest_forecasting_list):
    """
    Send the latest forecasting according to the farm owner's address and producing corp

    Parameters:
        latest_forecasting_list(list): list of Forecasting model instances

    Returns:
        None
    """
    owners = User.objects.filter(is_staff=False)  # TODO: 왈러스 연산자 사용해서 리팩토링 시도
    for owner in owners:
        farms = Farm.objects.filter(owner=owner)
        for farm in farms:
            producing_crops = ProducingCrop.objects.filter(farm=farm)
            for producing_crop in producing_crops:
                for forecasting in latest_forecasting_list:
                    sigungu_name = farm.medium_category_address
                    crop_name = producing_crop.crop.name
                    if forecasting.crop_name == crop_name and forecasting.sigungu_name == sigungu_name:
                        owner_number = owner.phone_number
                        forecasting_massage = forecasting.__str__()
                        _send_sms(owner_number, forecasting_massage)


def _make_signature(access_key, secret_key, method, uri, timestamp):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    result = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return result


def _send_sms(to_number, content):
    base_url = os.environ.get("SENS_URL")
    access_key = os.environ.get("SENS_ACCESS_KEY")
    secret_key = os.environ.get("SENS_SECRET_KEY")
    service_id = os.environ.get("SENS_SERVICE_ID")
    from_number = os.environ.get("SENS_FROM_NUMBER")
    uri = f"/sms/v2/services/{service_id}/messages"
    full_uri = base_url + uri
    timestamp = str(int(time.time() * 1000))

    body = {
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

    signature = _make_signature(access_key, secret_key, 'POST', uri, timestamp)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature
    }

    res = requests.post(full_uri, json=body, headers=headers)
    return res.json()
