from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_raw_reply_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Creates keyboard with buttons(items) in one line
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=True)
