import base64
import hashlib
import hmac
import os
import time

import requests

from accounts.models import User
from forecasting.models import Farm, ProducingCrop
from forecasting.models.farms import MediumCategoryAddress


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
                    # TODO: DB에 address code와 crop code 갱신 후, __dict__ 대신 '.'으로 속성 조회
                    medium_address_in_farm = farm.__dict__.get("medium_category_address_id")
                    medium_address_in_forecasting = forecasting.__dict__.get("medium_category_address_id")
                    crop_in_producing_crop = producing_crop.__dict__.get("crop_id")
                    crop_in_forecasting = forecasting.__dict__.get("crop_id")
                    if crop_in_producing_crop == crop_in_forecasting and medium_address_in_farm == medium_address_in_forecasting:
                        owner_number = owner.phone_number
                        forecasting_massage = forecasting.__str__()
                        send_sms(owner_number, forecasting_massage)


def send_sms(to_number, content):
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


def _make_signature(access_key, secret_key, method, uri, timestamp):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    result = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return result
