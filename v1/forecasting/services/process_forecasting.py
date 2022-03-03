import os
import requests
from datetime import date, datetime

from django.db import transaction
import xml.etree.ElementTree as elemTree

from forecasting.models import Forecasting
from forecasting.services.process_sms import send_forecasting_to_owners
from forecasting.services.utils import convert_text_to_data_structure


@transaction.atomic
def process_latest_forecasting():
    """
    Check the latest forecasting, Send the one with SMS and Save in DB

    Parameters:

    Returns:
        None
    """
    api_key, headers, url = _get_request_variables()
    forecasting_list = _get_basic_forecasting_results(api_key, headers, url)
    latest_date_in_api = _get_date_of_latest_forecasting(forecasting_list)

    if latest_date_in_api is None:
        return None

    if not _is_latest_data(latest_date_in_api):
        return None

    with transaction.atomic():
        latest_forecasting_list = _get_latest_forecasting(api_key, headers, latest_date_in_api, url)
        send_forecasting_to_owners(latest_forecasting_list)
        # Forecasting.objects.bulk_create(latest_forecasting_list) # TODO: 테스트 편리를 위한 주석추가


def _get_latest_forecasting(api_key, headers, latest_date_in_api, url):
    refined_forecasting_list = []
    forecasting_list = _get_basic_forecasting_results(api_key, headers, url)
    latest_date_text = latest_date_in_api.strftime('%Y%m%d')

    for idx, item in enumerate(forecasting_list):  # TODO: 테스트 편리를 위해 enumerate로 idx 추가
        # 메모리 한계 상 idx > 60 조건이 최대치임(6개월치 예찰정보 처리량)
        if idx > 3:  # TODO: 테스트 편리를 위해 idx > x 조건 추가
            break

        # if latest_date_text != item.find('inputStdrDatetm').text: # TODO: 테스트 종료 후, 최신날짜의 예찰정보만 취급하도록 주석 제거
        #     continue

        forecasting_date, crop_code, detail_key = _get_forecasting_variables(item)
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

                _append_instance_in_list(forecasting_date, refined_forecasting_list, crop_code, item, target)
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
    crop_code = item.find('kncrCode').text

    return forecasting_date, crop_code, detail_key


def _get_request_variables():
    url = "http://ncpms.rda.go.kr/npmsAPI/service"
    headers = {"Content-Type": "application/xml"}
    api_key = os.environ.get("PUBLIC_API_KEY")
    if api_key is None:
        raise

    return api_key, headers, url


def _append_instance_in_list(date, bulk_creating_list, crop_code, item, target):
    forecasting = Forecasting(
        date=datetime.strptime(date, '%Y%m%d').date(),
        medium_category_address_id=int(item.get("sigunguCode")),
        crop_id=crop_code,
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
    sigungu_forecasting_list = convert_text_to_data_structure(sigungu_text_list)

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
    sido_forecasting_list = convert_text_to_data_structure(sido_text_list)

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
