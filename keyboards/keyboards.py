from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def kb_builder(btns):
    builder = ReplyKeyboardBuilder()

    for btn in btns:
        builder.row(KeyboardButton(text=btn))

    return builder.as_markup()

main_kb = kb_builder(['Прогноз на сегодня', 'Прогноз на завтра', 'Прогноз на 5 дней'])