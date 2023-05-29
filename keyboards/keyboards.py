from time import process_time_ns
from typing import List
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def kb_builder(btns: List | List[List]):
    kb = []

    if type(btns[0]) == list:
        for btn_l in btns:
            row = []
            for btn in btn_l:
                row.append(KeyboardButton(text=btn))
            kb.append(row)
    else:
        for btn in btns:
            kb.append([KeyboardButton(text=btn)])

    return ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,is_persistent=True)

def inline_kb_builder(btns):
    inline_kb = []

    for text, cb_data in btns.items():
        inline_kb.append([InlineKeyboardButton(text=text, callback_data=cb_data)])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

main_kb = kb_builder(btns=[['Погода сейчас', 'Прогноз на завтра'], ['Прогноз на 5 дней'], ['Подключить уведомления']])