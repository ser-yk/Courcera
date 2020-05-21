import requests
from xml.etree import ElementTree

def get_currency_rate(id: str="R01200", date: str=None) -> str:
    try:
        params = {'date_req': date}
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params)
        root = ElementTree.fromstring(response.content)
        for valute in root.findall('Valute'):
            if valute.get('ID') == id:
                return 'Курс: {} руб.'.format(valute.find('Value').text)
        return 'Такого ID нет'
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.InvalidSchema):
        return 'Не удалось связаться с сайтом'


print(get_currency_rate())
