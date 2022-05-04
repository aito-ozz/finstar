import requests
import xmlschema
import xml.etree.ElementTree as ET
from pip import main
import pytest
from src.enum.global_enums import *
from configurations import *


def test_status_code():
    list_links = [
        xml_daily,
        val_curs,
        xml_val,
        valuta
    ]

    for link in list_links:
        responce = requests.get(link)
        assert responce.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value


def test_xms_daily_is_valid():
    responce = ET.fromstring(requests.get(xml_daily).text)
    xsd = xmlschema.XMLSchema(val_curs)

    assert xsd.is_valid(responce), GlobalErrorMessages.MATCHING_ERROR.value


def test_xml_valute_is_valid():
    responce = ET.fromstring(requests.get(xml_val).text)
    xsd = xmlschema.XMLSchema(valuta)

    assert xsd.is_valid(responce), GlobalErrorMessages.MATCHING_ERROR.value


def value_matching():
    tree = ET.ElementTree(requests.get(xml_daily))


# if __name__ == '__main__':
#     pytest.main()