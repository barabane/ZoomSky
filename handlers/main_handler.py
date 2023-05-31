import asyncio
from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from tzlocal import get_localzone

from bot_settings import scheduler, bot
from database.db import db
from api.weather import weather
from keyboards.keyboards import main_kb
from utils.templates.weather_template import forecast_template, today_template

router = Router()


async def notifications(user_id):
    db.subscribe_to_notifi(user_id)
    coordinates = db.get_user(user_id)[4].split(sep=',')
    today = weather.today_weather(user_data={
        'lat': coordinates[0],
        'lon': coordinates[1]
    })

    await bot.send_message(user_id, text=today_template(today), parse_mode='HTML')


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

    await msg.answer(text=today_template(today), parse_mode='HTML')


@router.message(F.text == 'Прогноз на завтра')
async def tomorrow_weather(msg: types.Message):
    city_name = db.get_user(msg.from_user.id)[3]
    tomorrow = weather.tomorrow_weather(city_name=city_name)[0]

    await msg.answer(text=forecast_template(tomorrow), parse_mode='HTML')


@router.message(F.text == 'Прогноз на 5 дней')
async def week_weather(msg: types.Message):
    city_name = db.get_user(msg.from_user.id)[3]
    week = weather.week_weather(city_name=city_name)

    for day in week:
        await msg.answer(text=forecast_template(day), parse_mode='HTML')
        await asyncio.sleep(1)


@router.message(F.text == 'Подключить уведомления')
async def subscribe(msg: types.Message):
    is_subscribed = db.get_user(msg.from_user.id)[5]

    if is_subscribed == 1:
        return await msg.answer('Уведомления уже подключены')

    scheduler.add_job(notifications, 'cron', hour=8, minute=0, args=[
                      msg.from_user.id], id='my_job', timezone=get_localzone())
    await msg.answer('Уведомления о погоде будут приходить каждый день в 8 часов утра')
