from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

ib1 = KeyboardButton(text='Отмена')

ikb.add(ib1)