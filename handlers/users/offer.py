from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.send_offer_to_admins import send_offer_to_admin_chat


class FSMOffer(StatesGroup):
    offer = State()


@dp.message_handler(commands=["offer"])
async def offer(message: types.Message):
    await FSMOffer.offer.set()
    await message.answer("Отправьте мне ваше объявление.")


@dp.message_handler(state=FSMOffer.offer)
async def load_offer(message: types.Message, state: FSMContext):
    await send_offer_to_admin_chat(message.text, str(message.from_id))
    await state.finish()
    await message.answer("Объявление отправлено на рассмотрение.")
