import asyncio
from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import CommandStart

from database.db import db
from api.weather import weather
from keyboards.keyboards import main_kb

router = Router()


@router.message(CommandStart())
async def start_handler(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(
                text='Отправить координаты 📍', request_location=True)
        ]
    ], resize_keyboard=True, one_time_keyboard=True)

    if db.get_user(msg.from_user.id) == None:
        return await msg.answer(text='Для начала, необходимо получить ваши координаты', reply_markup=keyboard)

    await msg.answer('Главное меню:', reply_markup=main_kb)


@router.message(F.location)
async def func(msg: types.Message):
    city_name = weather.today_weather({
        'lat': msg.location.latitude,
        'lon': msg.location.longitude
    })['location']['name']

    db.update_user({'id': msg.from_user.id, 'username': msg.from_user.username, 'reg_date': datetime.now(
    ), 'city_name': city_name, 'coordinates': f'{msg.location.latitude},{msg.location.longitude}'})

    await msg.answer(text='Главное меню:', reply_markup=main_kb)


@router.message(F.text == 'Погода сейчас')
async def today_weather(msg: types.Message):
    coordinates = db.get_user(msg.from_user.id)[4].split(sep=',')
    today = weather.today_weather(user_data={
        'lat': coordinates[0],
        'lon': coordinates[1]
    })

    await msg.answer(text=f"""
    📍<b>Город:</b> {today['location']['name']}\b
⌚️<b>Дата и время:</b> {today['location']['localtime']}
➖➖➖➖➖➖➖➖➖➖➖➖
⛅️Погода: <b>{today['current']['condition']['text']}</b>
🌡 Температура: {today['current']['temp_c']} °C
🙆‍♂️ Ощущается как: {today['current']['feelslike_c']} °C
🌬 Ветер: {today['current']['wind_mph']}\b м/с
👁 Видимость: {today['current']['vis_km']} км
""", parse_mode='HTML')


@router.message(F.text == 'Прогноз на завтра')
async def tomorrow_weather(msg: types.Message):
    city_name = db.get_user(msg.from_user.id)[3]
    tomorrow = weather.tomorrow_weather(city_name=city_name)[0]

    await msg.answer(text=f"""
    ⌚️<b>Дата: </b> {tomorrow['date']}
➖➖➖➖➖➖➖➖➖➖➖➖
⛅️Погода: <b>{tomorrow['day']['condition']['text']}</b>
🔥Макс. температура: {tomorrow['day']['maxtemp_c']} °C
🧊Мин. температура: {tomorrow['day']['mintemp_c']} °C
🌄Рассвет: {tomorrow['astro']['sunrise']}
🌅Закат: {tomorrow['astro']['sunset']}
""", parse_mode='HTML')


@router.message(F.text == 'Прогноз на 5 дней')
async def week_weather(msg: types.Message):
    city_name = db.get_user(msg.from_user.id)[3]
    week = weather.week_weather(city_name=city_name)

    for day in week:
        await msg.answer(text=f"""
            ⌚️<b>Дата: </b> {day['date']}
➖➖➖➖➖➖➖➖➖➖➖➖
⛅️Погода: <b>{day['day']['condition']['text']}</b>
🔥Макс. температура: {day['day']['maxtemp_c']} °C
🧊Мин. температура: {day['day']['mintemp_c']} °C
🌄Рассвет: {day['astro']['sunrise']}
🌅Закат: {day['astro']['sunset']}
""", parse_mode='HTML')
        await asyncio.sleep(1)
