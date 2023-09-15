# 1) Подключіться до API НБУ  отримайте теперішній курс валют и
# запишіть його в TXT-файл опціонально передбачте для користувача можливість обирати дату,
# на яку він хоче отримати курс
import requests
from datetime import datetime


class User:
    def today_date(self):
        date = int(datetime.now().strftime('%Y%m%d'))
        return date

    def cycle_user_input(self):
        max_attempts = 3
        attempts = 0
        current_date = self.today_date()
        while attempts <= max_attempts:
            try:
                user_input = input('Enter the date in YYYYMMDD format (for example, 20220913): ')
                if user_input.isdigit():
                    user_input = int(user_input)
                    if 20210301 <= user_input <= current_date:
                        return user_input
                    else:
                        print('Wrong! Enter a number between 20210301 and', current_date)
                        attempts += 1
                else:
                    print('Wrong! Enter a NUMBER!')
                    attempts += 1
                remaining_attempts = max_attempts - attempts
                print(f"Remaining attempts: {remaining_attempts}")
            except ValueError:
                print("Enter a valid number from 20210301 to", current_date)
        print("Exceeded maximum attempts")
        exit()


class NBU:
    def request_and_record(self, date):
        try:
            url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date={date}'
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            return f'Error: {e}'

        try:
            json_data = response.json()
        except Exception as e:
            return f'Error: {e}'

        with open('application.json', 'wb') as file:
            file.write(response.content)

        return json_data

    def cycle(self, json):
        currency_dict = {}
        for currency_data in json:
            currency_name = currency_data['txt']
            currency_rate = currency_data['rate']
            currency_dict[currency_name] = currency_rate
        return currency_dict

    def write_currency_txt(self, currency_rates_dict, date):
        filename = f"exchange_rates_{date}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"[дата, на яку актуальний курс]: {date}\n\n")
            for i, (currency, rate) in enumerate(currency_rates_dict.items(), start=1):
                file.write(f"{i}. {currency} to UAH: {rate}\n")


user_1 = User()
date = user_1.cycle_user_input()

nbu_1 = NBU()
json_data = nbu_1.request_and_record(date)
currency_rates_dict = nbu_1.cycle(json_data)
nbu_1.write_currency_txt(currency_rates_dict, date)
