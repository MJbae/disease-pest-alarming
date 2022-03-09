import os
from typing import Set, Optional
from datetime import datetime, date

import requests
import xml.etree.ElementTree as elemTree

from forecasting.domains import ForecastingDto, AffectedFarmDto
from forecasting.exceptions import DateNotFoundException, NotLatestException
from forecasting.models import Forecasting, User, Farm, Crop, ProducingCrop
from forecasting.utils import convert_text_to_list


def collect_the_latest_forecasting() -> Set[ForecastingDto]:
    api_key, headers, url = _get_request_vars()
    forecasting_generator = _get_forecasting_generator(api_key, headers, url)
    latest_date_from_source = _get_the_latest_forecasting_date(forecasting_generator)

    if latest_date_from_source is None:
        raise DateNotFoundException("Fail to find date field in forecasting source")

    if not _is_latest_forecasting(latest_date_from_source):
        raise NotLatestException(f"{latest_date_from_source} is not the latest forecasting")

    latest_forecasting_set = _get_latest_forecasting_set(api_key, headers, latest_date_from_source, url)

    return latest_forecasting_set


def _get_latest_forecasting_set(api_key, headers, latest_date_in_api, url) -> Set[ForecastingDto]:
    refined_forecasting_set = set()
    forecasting_generator = _get_forecasting_generator(api_key, headers, url)
    latest_date_text = latest_date_in_api.strftime('%Y%m%d')

    # 테스트 편리를 위해 enumerate로 idx 추가
    for idx, item in enumerate(forecasting_generator):
        # 테스트 편리를 위해 idx > x 조건 추가 / 메모리 한계 상 idx > 60 조건이 최대치임(6개월치 예찰정보 처리량)
        # if idx > 3:
        #     break

        if latest_date_text != item.find('inputStdrDatetm').text:
            continue

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

                _append_instance_in_list(forecasting_date, refined_forecasting_set, crop_code, item, target)
    return refined_forecasting_set


def _get_the_latest_forecasting_date(forecasting_list) -> Optional[date]:
    max_date = None
    for item in forecasting_list:
        date_in_text = item.find('inputStdrDatetm').text
        date = datetime.strptime(date_in_text, '%Y%m%d').date()
        if max_date is None:
            max_date = date
        if date > max_date:
            max_date = date

    return max_date


def _is_latest_forecasting(date_in_api):
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


def _get_request_vars():
    url = "http://ncpms.rda.go.kr/npmsAPI/service"
    headers = {"Content-Type": "application/xml"}
    api_key = os.environ.get("PUBLIC_API_KEY")
    if api_key is None:
        raise

    return api_key, headers, url


def _append_instance_in_list(date, bulk_creating_set, crop_code, item, target):
    forecasting = ForecastingDto(
        date=datetime.strptime(date, '%Y%m%d').date(),
        address_name=item.get("sigunguNm"),
        crop_name=crop_code,
        target_name=target,
    )
    bulk_creating_set.add(forecasting)
    return bulk_creating_set


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
    sigungu_forecasting_list = convert_text_to_list(sigungu_text_list)

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
    sido_forecasting_list = convert_text_to_list(sido_text_list)

    return sido_forecasting_list


def _get_forecasting_generator(api_key, headers, url):
    path_params = {
        "apiKey": api_key,
        "serviceCode": "SVC51",
        "serviceType": "AA001:XML",
        "searchExaminYear": date.today().year - 1,  # TODO: 테스트 편의를 위해 -1 적용
    }
    response = requests.get(url=url, params=path_params, headers=headers)
    tree = elemTree.fromstring(response.content)
    forecasting_generator = tree.iter(tag="item")

    return forecasting_generator
