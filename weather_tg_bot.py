import requests
import datetime
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from forecast import *
from keyboards import *

tg_bot = Bot(token='5888133619:AAE1XW55jVt-pqpkXma1PcmoNGFK8m0v9eE')
dp = Dispatcher(tg_bot)

kb = InlineKeyboardMarkup
inline_btn_1 = InlineKeyboardButton('Подробнее ..', callback_data='button_more')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await message.reply("Привет! Пришли название города, а я в ответ сводку его погоды!")

@dp.message_handler()
async def show_weather(message: types.Message):

    try:
        response_weather_en = requests.get(
            url=f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid=0d863b433525d8e7bd171eb04e479015&units=metric').json()

        response_weather = requests.get(
            url=f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid=0d863b433525d8e7bd171eb04e479015&units=metric&lang=ru').json()
        # await message.reply(response_weather)

        icons_weather = {
            'Clear': '☀',
            'Clouds': '☁',
            'Fog': '🌥',
            'Snow': '🌨',
            'Rain': '🌧',
            'Drizzle': '🌬',
            'Thunderstorm': '⛈',

        }

        main_weather = response_weather['weather'][0]['main']
        if main_weather in icons_weather:
            icon_ = icons_weather[main_weather]
        else:
            icon_ = "выгляни в окно ✨"

        global country_code, city_en, weather_more

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

        await message.reply(f'\U0001F682\U0001F682\U0001F682\U0001F682\U0001F682 {datetime.now().strftime("%d.%m.%Y %H:%M")} \U0001F682\U0001F682\U0001F682\U0001F682\U0001F682'
              f' \nТекущая погода в городе {city} {icon_}: \n сейчас {state}, небо затянуто облаками на {clouds}%; \n текущая температура: '
              f'{temp}°C, атм. давление: {pressure} мм рт. ст.;  \n влажность: {humidity}%, скорость ветра: {wind_speed} м/с; \n время '
              f'восхода солнца: {sunrise.time()}, заката: {sunset.time()}, продолжительность дня: {day_time}.', reply_markup=inline_kb1)

        weather_more = forecast_show(country_code, city_en)

        # with open('weather.json', 'w') as file:
        #     json.dump(response_weather, file, indent=4, ensure_ascii=False)

    except Exception as _ex:
        await message.reply(str(_ex))
        await message.reply('❗ Проверьте название города ❗')

@dp.callback_query_handler(lambda c: c.data == 'button_more')
async def process_callback_button1(callback_query: types.CallbackQuery):

    await tg_bot.answer_callback_query(callback_query.id)
    await tg_bot.send_message(callback_query.from_user.id, weather_more)

if __name__ == '__main__':
    executor.start_polling(dp)