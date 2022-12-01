from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


def create_raw_vote_keyboard(author_id: str, message_id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(text="Одобрить",
                               callback_data=f"voteon-{author_id}-{message_id}"
                               )

    ib2 = InlineKeyboardButton(text="Отклонить",
                               callback_data=f"voteoff-{author_id}-{message_id}"
                               )

    return ikb.add(ib1, ib2)
