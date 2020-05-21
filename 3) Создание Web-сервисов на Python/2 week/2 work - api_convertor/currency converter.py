from bs4 import BeautifulSoup
from decimal import Decimal

import requests


def convert(amount, cur_from, cur_to, date, requests):
    amount = Decimal(amount)
    params = {'date_req': date}
    response = requests.get('https://www.cbr.ru/scripts/XML_daily_eng.asp', params)  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    if cur_from == 'RUR':
        amount_cur_from = amount
    else:
        cur_from_soup = soup.find('CharCode', text=cur_from)
        cur_from = Decimal(cur_from_soup.find_next_sibling('Value').string.replace(',', '.'))
        nominal_cur_to = Decimal(cur_from_soup.find_next_sibling('Nominal').string)
        amount_cur_from = cur_from / nominal_cur_to * amount

    cur_to_soup = soup.find('CharCode', text=cur_to)
    cur_to = Decimal(cur_to_soup.find_next_sibling('Value').string.replace(',', '.'))
    nominal_cur_to = Decimal(cur_to_soup.find_next_sibling('Nominal').string)
    amount_cur_to = cur_to / nominal_cur_to

    result = amount_cur_from / amount_cur_to
    return result.quantize(Decimal("1.0000"))  # не забыть про округление до 4х знаков после запятой


print('My result:', convert(50, 'USD', 'EUR', "16/05/2020", requests))

