from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_open_dm_button(chat_id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)

    ib1 = InlineKeyboardButton(text='Перейти к продавцу',
                               url=f'tg://openmessage?user_id={chat_id}')

    return ikb.add(ib1)
