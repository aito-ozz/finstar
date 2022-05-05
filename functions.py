# from locale import currency
from required import *
from configurations import *


#Создаем словарь с кодом и курсом валют из ежедневной котировки
def get_data(url):
    web_file = urllib.request.urlopen(url)
    return web_file.read()

def get_currencies_dictionary(xml_content):

    dom = minidom.parseString(xml_content)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict


def print_dict(dict):
    for key in dict.keys():
        print(key, dict[key])

# def exchange_rate(dict):
#     for key in dict:
#         if dict[key] == int([key]):
#             print(dict[key])

if __name__ == '__main__':
    # url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    currency_dict = get_currencies_dictionary(get_data(xml_daily))
    print_dict(currency_dict)
    # exchange_rate(currency_dict)
