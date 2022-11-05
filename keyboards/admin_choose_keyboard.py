from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


def create_raw_vote_keyboard(mesid: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(text="Одобрить",
                               callback_data=f"voteon-{mesid}"
                               )

    ib2 = InlineKeyboardButton(text="Отклонить",
                               callback_data=f"voteoff-{mesid}"
                               )

    return ikb.add(ib1, ib2)
