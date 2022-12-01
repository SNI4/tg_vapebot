from loader import bot
from aiogram.types import MediaGroup
from data.config import ADMIN_CHAT_ID, ADMIN_CHAT_CHOOSE
from utils.misc.json_worker import save_json
from keyboards.admin_choose_keyboard import create_raw_vote_keyboard


async def send_advert_to_admins(data: dict) -> None:
    channel = await bot.get_chat(data['channel_to'])
    raw_msg = f'''
#Продаю
🏴 Регион: #{channel.title}
👨 От {data["user_mention"]}      
❗ {data["name"]} ❗
✔ Cостояние: {data["condition"]}/10
💸 Цена: {data["price"]}₽
📃 Описание:
{data["description"]}
'''

    group = MediaGroup()
    for num in range(len(data['media'])):
        group.attach_photo(data['media'][num], caption=raw_msg if num == 0 else '')

    media_msg = await bot.send_media_group(media=group, chat_id=ADMIN_CHAT_ID)

    choose_msg = await bot.send_message(chat_id=ADMIN_CHAT_ID, text=ADMIN_CHAT_CHOOSE)
    await choose_msg.edit_reply_markup(create_raw_vote_keyboard(
        author_id=data['user_id'],
        message_id=choose_msg.message_id))

    await save_json(user_id=str(data['user_id']),
                    message_id=choose_msg.message_id,
                    second_messages_id=[k["message_id"] for k in media_msg],
                    data=data)
