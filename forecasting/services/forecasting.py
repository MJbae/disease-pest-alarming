import os
import requests
import time
import base64
import hmac
import hashlib

import xml.etree.ElementTree as elemTree
from datetime import date, datetime

from accounts.models import User
from forecasting.models import Forecasting, Farm, ProducingCrop


def catch_latest_forecasting():
    # 올해 예찰정보 리스트 조회
    api_key, headers, url = _get_request_variables()
    forecasting_list = _get_basic_forecasting_results(api_key, headers, url)
    latest_date_in_api = _get_date_of_latest_forecasting(forecasting_list)

    # 예찰 정보가 없을 시 메소드 종료
    if latest_date_in_api is None:
        return None

    # 최신 업데이트 내용이 없을 시 메소드 종료
    if not _is_latest_data(latest_date_in_api):
        return None

    # 최신 예찰정보 조회
    latest_forecasting_list = _get_latest_forecasting(api_key, headers, latest_date_in_api, url)

    # 연관 회원에게 예찰정보 전송
    owners = User.objects.filter(is_staff=False)
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

    # 최신 업데이트 내용을 DB에 반영
    # Forecasting.objects.bulk_create(latest_forecasting_list) #


def _make_signature(access_key, secret_key, method, uri, timestamp):
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    result = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return result


def _send_sms(to_number, content):
    print(f'to: {to_number}')
    print(f'content: {content}')
    print(f'')

    base_url = os.environ.get("SENS_URL")
    access_key = os.environ.get("SENS_ACCESS_KEY")
    secret_key = os.environ.get("SENS_SECRET_KEY")
    from_number = os.environ.get("SENS_FROM_NUMBER")
    uri = f"{base_url}/services/{access_key}/messages"
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

    res = requests.post(uri, json=body, headers=headers)
    print(res.json())
    return res.json()


def _get_latest_forecasting(api_key, headers, latest_date_in_api, url):
    refined_forecasting_list = []
    forecasting_list = _get_basic_forecasting_results(api_key, headers, url)
    latest_date_text = latest_date_in_api.strftime('%Y%m%d')

    for idx, item in enumerate(forecasting_list):  # TODO: 테스트 편리를 위해 enumerate로 idx 추가

        if idx > 2:  # TODO: 테스트 편리를 위해 idx > 5 조건 추가
            break
        # if latest_date_text != item.find('inputStdrDatetm').text: # TODO: 테스트 종료 후, 최신날짜의 예찰정보만 취급하도록 주석 제거
        #     continue

        forecasting_date, crop_code, crop_name, detail_key = _get_forecasting_variables(item)
        sido_forecasting_list = _get_sido_forecasting_results(api_key, detail_key, headers, url)
        pre_sido = "&^%"
        for item in sido_forecasting_list:
            sido = item.get("sidoNm")
            if pre_sido == sido:
                continue

            pre_sido = sido

            if item.get("inqireValue") == "0":
                continue

            sigungu_forecasting_list = _get_sigungu_forecasting_results(api_key, detail_key, headers, item, url)
            pre_target = "&^%"
            for item in sigungu_forecasting_list:
                target = item.get("dbyhsNm")
                if pre_target in target:
                    continue

                idx = target.find("(")
                target = target[:idx]
                pre_target = target

                if item.get("inqireValue") == "0":
                    continue

                _append_instance_in_list(forecasting_date, refined_forecasting_list, crop_code, crop_name, item, target)
    return refined_forecasting_list


def _get_date_of_latest_forecasting(forecasting_list):
    max_date = None
    for item in forecasting_list:
        date_in_text = item.find('inputStdrDatetm').text
        date = datetime.strptime(date_in_text, '%Y%m%d').date()
        if max_date is None:
            max_date = date
        if date > max_date:
            max_date = date

    return max_date


def _is_latest_data(date_in_api):
    # forecasting record 내 조사 날짜 컬럼 추가
    # 기존 DB 내 최신 forecasting 날짜와 api 호출에 따른 forecasting의 날짜를 비교해서 최선여부 확인할 것
    latest_forecasting = Forecasting.objects.latest("date")
    date_in_db = latest_forecasting.date

    return True if date_in_api > date_in_db else False


def _get_forecasting_variables(item):
    forecasting_date = item.find('inputStdrDatetm').text
    detail_key = item.find('insectKey').text
    crop_name = item.find('kncrNm').text
    crop_code = item.find('kncrCode').text

    return forecasting_date, crop_code, crop_name, detail_key


def _get_request_variables():
    url = "http://ncpms.rda.go.kr/npmsAPI/service"
    headers = {"Content-Type": "application/xml"}
    api_key = os.environ.get("PUBLIC_API_KEY")
    if api_key is None:
        raise

    return api_key, headers, url


def _append_instance_in_list(date, bulk_creating_list, crop_code, crop_name, item, target):
    forecasting = Forecasting(
        date=datetime.strptime(date, '%Y%m%d').date(),
        sigungu_name=item.get("sigunguNm"),
        sigungu_code=item.get("sigunguCode"),
        crop_name=crop_name,
        crop_code=crop_code,
        target=target,
    )

    bulk_creating_list.append(forecasting)


def _get_sigungu_forecasting_results(api_key, detail_key, headers, item, url):
    sido_code = item.get("sidoCode")
    sigungu_path_params = {
        "apiKey": api_key,
        "serviceCode": "SVC53",
        "serviceType": "AA001:XML",
        "insectKey": detail_key,
        "sidoCode": sido_code
    }
    sigungu_response = requests.get(url=url, params=sigungu_path_params, headers=headers)
    sigungu_tree = elemTree.fromstring(sigungu_response.content)
    sigungu_text_list = sigungu_tree.find('list').text
    sigungu_forecasting_list = _convert_text_to_data_structure(sigungu_text_list)

    return sigungu_forecasting_list


def _get_sido_forecasting_results(api_key, detail_key, headers, url):
    sido_path_params = {
        "apiKey": api_key,
        "serviceCode": "SVC52",
        "serviceType": "AA001:XML",
        "insectKey": detail_key,
    }
    sido_response = requests.get(url=url, params=sido_path_params, headers=headers)
    sido_tree = elemTree.fromstring(sido_response.content)
    sido_text_list = sido_tree.find('list').text
    sido_forecasting_list = _convert_text_to_data_structure(sido_text_list)

    return sido_forecasting_list


def _get_basic_forecasting_results(api_key, headers, url):
    path_params = {
        "apiKey": api_key,
        "serviceCode": "SVC51",
        "serviceType": "AA001:XML",
        "searchExaminYear": date.today().year - 1,  # TODO: 테스트 편의를 위해 -1 적용
    }
    response = requests.get(url=url, params=path_params, headers=headers)
    tree = elemTree.fromstring(response.content)
    forecasting_list = tree.iter(tag="item")

    return forecasting_list


def _convert_text_to_data_structure(text):
    key_idx_start = 0
    key_idx_end = 0
    value_idx_start = 0
    value_idx_end = 0
    result = []
    temp_dict = {}

    for idx, char in enumerate(text):
        if char == "{":
            key_idx_start = idx + 1
        if char == ",":
            value_idx_end = idx
            key = text[key_idx_start:key_idx_end]
            value = text[value_idx_start:value_idx_end]
            temp_dict[key] = value
        if char == " ":
            key_idx_start = idx + 1
        if char == "=":
            key_idx_end = idx
            value_idx_start = idx + 1
        if char == "}":
            idx += 2
            key = text[key_idx_start:key_idx_end]
            value = text[value_idx_start:value_idx_end]
            temp_dict[key] = value
            result.append(temp_dict)
            temp_dict = {}

    return result
