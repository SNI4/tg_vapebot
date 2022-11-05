from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


def create_raw_vote_keyboard(mesid: str, content: str, author_id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(text="Одобрить",
                               callback_data=f"voteon-{mesid}-{content}-{author_id}"
                               )

    ib2 = InlineKeyboardButton(text="Отклонить",
                               callback_data=f"voteoff-{mesid}-{author_id}"
                               )

    return ikb.add(ib1, ib2)
