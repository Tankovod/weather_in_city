import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def show_weather(city='Minsk'):

    if city == '':
        city = 'Minsk'


    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    }



    try:
        response_weather_en = requests.get(
            url=f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0d863b433525d8e7bd171eb04e479015&units=metric').json()

        response_weather = requests.get(
            url=f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0d863b433525d8e7bd171eb04e479015&units=metric&lang=ru').json()
        print(response_weather)

        icons_weather = {
            'Clear': '☀',
            'Clouds': '☁',
            'Fog': '🌥',
            'Snow': '🌨',
            'Rain': '🌧',
            'Drizzle': '🌬',
            'Thunderstorm': '⛈',

        }

        city_en = slugify(response_weather_en['name'])
        country_code = response_weather['sys']['country'].lower()

        city = response_weather['name']
        state = response_weather['weather'][0]['description']
        clouds = response_weather['clouds']['all']
        temp = response_weather['main']['temp']
        pressure = response_weather['main']['pressure']
        humidity = response_weather['main']['humidity']
        wind_speed = response_weather['wind']['speed']
        sunrise = datetime.fromtimestamp(response_weather['sys']['sunrise'])
        sunset = datetime.fromtimestamp(response_weather['sys']['sunset'])
        day_time = datetime.fromtimestamp(response_weather['sys']['sunset']) - datetime.fromtimestamp(response_weather['sys']['sunrise'])

        response_forecast = requests.get(
            url=f'https://ru.meteotrend.com/forecast/{country_code}/{city_en}/', headers=headers
        )

        print(f'https://ru.meteotrend.com/forecast/{country_code}/{city_en}/')

        print(f'Текущая погода в городе {city}\U0001F608: \n сейчас {state}, небо затянуто облаками на {clouds}%; \n текущая температура: '
              f'{temp}C, атм. давление: {pressure} мм рт. ст.;  \n влажность: {humidity}%, скорость ветра: {wind_speed} м/с; \n время '
              f'восхода солнца: {sunrise.time()}, заката: {sunset.time()}, продолжительность дня: {day_time}.')


        src = response_forecast.text
        src = src.encode('UTF-8').decode('UTF-8')
        # print(src)

        soup = BeautifulSoup(src, 'lxml')
        forecast_text = soup.find_all(class_='foreca')
        print(forecast_text[10].text)

    except Exception as _ex:
        print(_ex)
        print('check the name of the city')


def main():
    city_name = input('enter the city name (Minsk) > ')
    show_weather(city_name)


if __name__ == '__main__':
    main()
