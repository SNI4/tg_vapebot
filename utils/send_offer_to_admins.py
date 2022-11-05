from data import config
from loader import bot


async def send_offer_to_admin_chat(content: str) -> None:
    Message = await bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                                     text=content)
