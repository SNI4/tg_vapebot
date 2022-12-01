import asyncio
import re
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from loader import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.dialogs_cfg import *
from utils.send_advert import send_advert_to_admins
from keyboards.create_raw_reply_keyboard import create_raw_reply_keyboard
from utils.misc.json_worker import get_json_keys_title_space, get_json_keys, get_json_value


async def action(message: types.Message, state: FSMContext):
    global is_runned

    async with state.proxy() as data:
        try:
            data['media'].append(message.photo[-1].file_id)
        except IndexError:
            await message.reply(WRONG_MEDIA, parse_mode='MarkdownV2')
            return

    if not is_runned:
        is_runned = True
        await asyncio.sleep(1.0)

        async with state.proxy() as data:
            user_data = {
                "user_mention": message.from_user.get_mention(),
                "user_id": message.from_user.id,
                "channel_to": data["channel_to"],
                "name": data["name"],
                "condition": data["condition"],
                "price": data["price"],
                "description": data["description"],
                "media": data["media"],
                "timestamp": time.time()
            }
        await send_advert_to_admins(data=user_data)
        await state.finish()

        await message.answer(OFFER_FINISH)
class FSMOffer(StatesGroup):
    channel_to = State()
    name = State()
    condition = State()
    price = State()
    description = State()
    media = State()


@dp.message_handler(commands=["offer"])
async def channel_to(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.chat.id)
    user_channel_status = re.findall(r"\w*", str(user_channel_status))

    try:
        if user_channel_status[70] != 'left':
            await FSMOffer.channel_to.set()
            await message.answer(CHOOSE_REGION, reply_markup=create_raw_reply_keyboard(
                await get_json_keys_title_space('regions_cfg')
            ))
        else:
            await message.answer(NEED_TO_SUBSCRIBE)
    except:
        if user_channel_status[60] != 'left':
            await FSMOffer.channel_to.set()
            await message.answer(CHOOSE_REGION, reply_markup=create_raw_reply_keyboard(
                await get_json_keys_title_space('regions_cfg')
            ))
        else:
            await message.answer(NEED_TO_SUBSCRIBE)


@dp.message_handler(state=FSMOffer.channel_to)
async def get_channel_to(message: types.Message, state: FSMContext):
    if message.text.lower().replace(' ', '_') in await get_json_keys('regions_cfg'):
        await state.update_data(channel_to=await get_json_value('regions_cfg', message.text.lower().replace(' ', '_')))
        await message.answer(SET_NAME)
        await FSMOffer.name.set()

    else:
        await message.answer(WRONG_REGION,
                             reply_markup=create_raw_reply_keyboard(
                                 await get_json_keys_title_space('regions_cfg')))


@dp.message_handler(state=FSMOffer.name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text.lower() == 'далее':
        await FSMOffer.condition.set()
        await message.answer(SET_CONDITION)

    else:
        title = message.text.title()
        await state.update_data(name=title)
        bot_msg = await message.answer(title)
        await bot_msg.reply(CONFIRM_NAME,
                            reply_markup=create_raw_reply_keyboard([YES_NAME_BUTTON]), )


@dp.message_handler(state=FSMOffer.condition)
async def get_condition(message: types.Message, state: FSMContext):
    if message.text in [str(i) for i in range(1, 11)]:
        await state.update_data(condition=message.text)

        await message.answer(SET_PRICE)
        await FSMOffer.price.set()

    else:
        await message.reply(WRONG_CONDITION)


@dp.message_handler(state=FSMOffer.price)
async def get_price(message: types.Message, state: FSMContext):
    if message.text.lower() == 'далее':
        await message.answer(SET_DESCRIPTION)
        await FSMOffer.description.set()

    elif message.text.isdigit():

        await state.update_data(price=message.text)

        await message.reply(CONFIRM_PRICE(message.text),
                            reply_markup=create_raw_reply_keyboard([YES_PRICE_BUTTON]),
                            parse_mode='MarkdownV2')

    else:
        await message.reply(WRONG_PRICE, parse_mode="MarkdownV2")


@dp.message_handler(state=FSMOffer.description)
async def get_description(message: types.Message, state: FSMContext):
    if message.text.lower() == 'далее':
        global is_runned

        await FSMOffer.media.set()
        await state.update_data(media=[])
        await message.answer(SET_MEDIA)

        is_runned = False

    else:
        await state.update_data(description=message.text)
        bot_msg = await message.answer(message.text)
        await bot_msg.reply(CONFIRM_DESCRIPTION,
                            reply_markup=create_raw_reply_keyboard([YES_DESCRIPTION_BUTTON]),
                            parse_mode="MarkdownV2")


@dp.message_handler(content_types=['any'], state=FSMOffer.media)
async def get_media(message: types.Message, state: FSMContext):
    await action(message, state)
