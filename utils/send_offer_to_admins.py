from data import config
from keyboards.admin_choose_keyboard import create_raw_vote_keyboard
from loader import bot


async def send_offer_to_admin_chat(content: str, author_id: str) -> None:
    Message = await bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                                     text=content)

    await Message.edit_reply_markup(create_raw_vote_keyboard(Message.message_id, content, author_id))
