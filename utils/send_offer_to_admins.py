from aiogram import types

from data import config
from keyboards.admin_choose_keyboard import create_raw_vote_keyboard
from loader import bot
from utils.misc import json_worker


async def send_offer_to_admin_chat(author_id: str) -> str:
    #data = get_json

    #group = types.MediaGroup()
    Message = await bot.send_media_group()

    #await Message.edit_reply_markup(create_raw_vote_keyboard(Message.message_id, content, author_id))
    return str(Message.id)
