# Импортируем зависимости
from required import *
# from functions import *
from src.enum.global_enums import GlobalErrorMessages as GEM


# Проверяем ответ от API
def test_status_code():
    list_links = [
        xml_daily,
        val_curs,
        xml_val,
        valuta
    ]

    for link in list_links:
        responce = requests.get(link)
        assert responce.status_code == status_code, GEM.WRONG_STATUS_CODE.value


# Сравнимаем XML файл ежедневных котировок с XSD схемой
def test_xms_daily_is_valid():
    responce = ET.fromstring(requests.get(xml_daily).text)
    xsd = xmlschema.XMLSchema(val_curs)

    assert xsd.is_valid(responce), GEM.MATCHING_ERROR.value


# Сравниваем XML файл валют с XSD схемой
def test_xml_valute_is_valid():
    responce = ET.fromstring(requests.get(xml_val).text)
    xsd = xmlschema.XMLSchema(valuta)

    assert xsd.is_valid(responce), GEM.MATCHING_ERROR.value


# Проверяем, что курс валют содержит числовые данные и коды валют реальны
def test_numbers_and_codes():
    # Создаем словарь с курсом и кодами валют
    daily_file = urllib.request.urlopen(xml_daily).read()
    
    dom_daily = minidom.parseString(daily_file)
    dom_daily.normalize()

    elements_daily = dom_daily.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements_daily:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = child.firstChild.data.replace(',', '.')
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value

    # Проверяем что курс валют это числовые данные
    for key in currency_dict.keys():
        if currency_dict[key].isdigit():
            continue
        else:
            assert float(currency_dict[key]), GEM.IS_NOT_DIGIT.value

    # Создаем список с ежедневными ISO кодами валют
    val_full_file = urllib.request.urlopen(val_full).read()

    dom_val_full = minidom.parseString(val_full_file)
    dom_val_full.normalize()

    elements_val_full = dom_val_full.getElementsByTagName("Item")
    val_full_list = []

    for node in elements_val_full:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'ISO_Char_Code':
                    if child.firstChild is not None:
                        if child.firstChild.nodeType == 3:
                            char_code = child.firstChild.data
                            val_full_list.append(char_code)
    

    # Проверяем, есть ли коды валют из словаря в списке с ISO кодами
    for key in currency_dict.keys():
        assert key in val_full_list, GEM.NON_EXISTENT_CURRENCY.value

if __name__ == '__main__':
    pytest.main()