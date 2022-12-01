from aiogram.types import MediaGroup

from data import config
from loader import dp, bot
from aiogram import types
from utils.misc.json_worker import get_advert_dict, delete_json
from data.config import *

@dp.callback_query_handler()
async def admin_vote_callback(callback: types.CallbackQuery):
    if callback.data.startswith('voteon'):
        stroka = callback.data.split('-')

        author_id = stroka[1]
        message_id = stroka[2]

        data = await get_advert_dict(message_id=message_id, user_id=author_id)
        channel = await bot.get_chat(data['channel_to'])
        # 🏴 Регион: #{channel.title}
        raw_msg = f'''
#Продаю
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

        await bot.send_media_group(media=group, chat_id=int(data['channel_to']))
        await callback.answer('Обьявление успешно выложено!')

        await bot.delete_message(config.ADMIN_CHAT_ID,
                                 message_id)

        for photo_id in data["second_messages_id"]:
            await bot.delete_message(message_id=photo_id, chat_id=ADMIN_CHAT_ID)

        await bot.send_message(author_id, "Ваше объявление было опубликовано!")

    elif callback.data.startswith('voteoff'):
        stroka = callback.data.split('-')

        author_id = stroka[1]
        message_id = stroka[2]

        data = await get_advert_dict(message_id=message_id, user_id=author_id)

        await bot.delete_message(config.ADMIN_CHAT_ID, message_id)
        for photo_id in data["second_messages_id"]:
            await bot.delete_message(message_id=photo_id, chat_id=ADMIN_CHAT_ID)
        await delete_json(author_id, message_id)
        await callback.answer('Объявление отклонено.')
        await bot.send_message(author_id, 'Ваше объявление было отклонено.')
