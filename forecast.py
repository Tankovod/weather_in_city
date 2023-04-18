import requests
from bs4 import BeautifulSoup
import re

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def forecast_show(country_code, city_en):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    }

    response_forecast = requests.get(
        url=f'https://ru.meteotrend.com/forecast/{country_code}/{city_en}/', headers=headers
    )

    src = response_forecast.text
    src = src.encode('UTF-8').decode('UTF-8')
    # print(src)

    soup = BeautifulSoup(src, 'lxml')
    forecast_text = soup.find_all(class_='foreca')

    return forecast_text[0].text