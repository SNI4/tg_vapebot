import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from loader import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.send_offer_to_admins import send_offer_to_admin_chat
from keyboards.cancel_keyboard import ikb

class FSMOffer(StatesGroup):
    offer = State()


@dp.message_handler(commands=["offer"])
async def offer(message: types.Message):

    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.chat.id)
    user_channel_status = re.findall(r"\w*", str(user_channel_status))
    try:
        if user_channel_status[70] != 'left':
            await FSMOffer.offer.set()
            await message.answer("Отправьте мне ваше объявление.", reply_markup=ikb)
        else:
            await message.answer('Вы не подписаны на канал!\nt.me/brxlkpsd')
    except:
        if user_channel_status[60] != 'left':
            await FSMOffer.offer.set()
            await message.answer("Отправьте мне ваше объявление.", reply_markup=ikb)
        else:
            await message.answer('Вы не подписаны на канал!\nt.me/brxlkpsd')


@dp.message_handler(state=FSMOffer.offer)
async def load_offer(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.reply('Successfuly canceled.')
        await state.finish()
    else:
        await send_offer_to_admin_chat(message.text, str(message.from_id))
        await state.finish()
        await message.answer("Объявление отправлено на рассмотрение.")
