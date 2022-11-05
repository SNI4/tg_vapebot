from aiogram import types

from keyboards.keyboard import ikb
from loader import dp


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Для того, чтобы предложить обьявление нажми на кнопку!",
                         reply_markup=ikb)


