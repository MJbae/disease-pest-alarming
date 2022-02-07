from datetime import date

import requests
import xml.etree.ElementTree as elemTree

from accounts.models import Setting
from forecasting.models import Forecasting


def refine_xml_from_forecasting_search():
    bulk_creating_list = []
    api_key, headers, url = _get_request_variables()

    forecasting_list = _get_basic_forecasting_results(api_key, headers, url)
    for idx, item in enumerate(forecasting_list):
        if idx > 5:
            break

        crop_code, crop_name, detail_key = _get_crop_variables(item)

        sido_forecasting_list = _get_sido_forecasting_results(api_key, detail_key, headers, url)
        for item in sido_forecasting_list:
            if item.get("inqireValue") == "0":
                continue

            sigungu_forecasting_list = _get_sigungu_forecasting_results(api_key, detail_key, headers, item, url)
            for item in sigungu_forecasting_list:
                if item.get("inqireValue") == "0":
                    continue

                _append_instance_in_list(bulk_creating_list, crop_code, crop_name, item)

    Forecasting.objects.bulk_create(bulk_creating_list)


def _get_crop_variables(item):
    detail_key = item.find('insectKey').text
    crop_name = item.find('kncrNm').text
    crop_code = item.find('kncrCode').text

    return crop_code, crop_name, detail_key


def _get_request_variables():
    url = "http://ncpms.rda.go.kr/npmsAPI/service"
    headers = {"Content-Type": "application/xml"}
    api_key = Setting.objects.get(key="apiKey").value

    if api_key is None:
        raise

    return api_key, headers, url


def _append_instance_in_list(bulk_creating_list, crop_code, crop_name, item):
    target = item.get("dbyhsNm")
    idx = target.find("(")
    target = target[:idx]
    forecasting = Forecasting(
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
        "searchExaminYear": date.today().year,
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
