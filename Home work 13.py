# 1) Подключіться до API НБУ  отримайте теперішній курс валют и
# запишіть його в TXT-файл опціонально передбачте для користувача можливість обирати дату,
# на яку він хоче отримати курс
import requests
import pprint
from datetime import datetime


def request_and_record():
    try:
        response = requests.request('Get', 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
    except Exception as e:
        return f'Error, {e}'
    else:
        if 200 <= response.status_code < 300 and response.headers['Content-Type'] == 'application/json; charset=utf-8':
            try:
                json_data = response.json()
            except Exception as e:
                return f'Error, {e}'
            else:
                with open('application.json', 'wb') as file:
                    file.write(response.content)
            return json_data


def cycle(json):
    currency_dict = {}
    for currency_data in json:
        currency_name = currency_data['txt']
        currency_rate = currency_data['rate']
        currency_dict[currency_name] = currency_rate
    return currency_dict

def write_currency_txt(currency_rates_dict, date):
    filename = f"exchange_rates_{date}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"[дата, на яку актуальний курс]: {date}\n\n")
        for i, (currency, rate) in enumerate(currency_rates_dict.items(), start=1):
            file.write(f"{i}. {currency} to UAH: {rate}\n")
    return None

date_input = input("Enter the date in YYYYMMDD format (for example, 20220913) or press Enter for the current date: ")
if not date_input:
    date_input = datetime.now().strftime("%Y%m%d")

json_data = request_and_record()
currency_rates_dict = cycle(json_data)

write_currency_txt(currency_rates_dict, date_input)


json_data = request_and_record()
currency_rates_dict = cycle(json_data)

pprint.pprint(currency_rates_dict)






