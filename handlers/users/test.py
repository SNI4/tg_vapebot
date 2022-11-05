import asyncio

from loader import dp, bot
from aiogram import types


@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    mes = await message.answer('123')
    await asyncio.sleep(2)
    await bot.delete_message(message.from_id, mes.message_id)
