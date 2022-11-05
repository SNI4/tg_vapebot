from data import config
from keyboards.open_dm_button import make_open_dm_button
from loader import dp, bot
from aiogram import types


@dp.callback_query_handler()
async def admin_vote_callback(callback: types.CallbackQuery):
    if callback.data.startswith('voteon'):
        data = callback.data.split('-')

        message_id = int(data[1])
        content = data[2]
        author_id = int(data[3])

        await bot.send_message(config.CHANNEL_ID,
                               content,
                               reply_markup=make_open_dm_button(str(author_id)))

        await callback.answer('Обьявление успешно выложено!')

        await bot.delete_message(config.ADMIN_CHAT_ID,
                                 message_id)

        await bot.send_message(author_id, "Ваше объявление было опубликовано!")

    elif callback.data.startswith('voteoff'):
        data = callback.data.split('-')

        message_id = int(data[1])
        author_id = int(data[2])

        await bot.delete_message(config.ADMIN_CHAT_ID, message_id)
        await callback.answer('Объявление отклонено.')
        await bot.send_message(author_id, 'Ваше объявление было отклонено.')