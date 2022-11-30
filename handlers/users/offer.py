import asyncio
import re
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from loader import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.send_offer_to_admins import send_offer_to_admin_chat
from keyboards.cancel_keyboard import ikb
from keyboards.create_raw_reply_keyboard import create_raw_reply_keyboard
from utils.misc.get_json import get_json_keys_title_space, get_json_keys, get_json_value


async def action(message: types.Message, state: FSMContext):
    global is_runned

    async with state.proxy() as data:
        try:
            data['media'].append(message.photo[-1].file_id)
        except IndexError:
            await message.reply('Отправьте __фото__', parse_mode='MarkdownV2')
            return

    if not is_runned:
        is_runned = True
        await asyncio.sleep(1.0)
        async with state.proxy() as data:
            group = types.MediaGroup()

            try:
                for photo_id in data['media']:
                    group.attach_photo(photo_id)

            except:
                await message.reply('Отправьте __фото__', parse_mode='MarkdownV2')
                return

        await state.finish()

        async with state.proxy() as data:
            user_data = {
                    "channel_to": data["channel"],
                    "name": data["name"],
                    "condition": data["condition"],
                    "price": data["price"],
                    "description": data["description"],
                    "media": data["media"],
                    "timestamp": time.time()
                }



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
            await message.answer("Выберите регион, в котором вы находитесь", reply_markup=create_raw_reply_keyboard(
                get_json_keys_title_space('regions_cfg')
            ))
        else:
            await message.answer('Вы не подписаны на канал!\nt.me/*******')
    except:
        if user_channel_status[60] != 'left':
            await FSMOffer.channel_to.set()
            await message.answer("Выберите регион, в котором вы находитесь", reply_markup=create_raw_reply_keyboard(
                get_json_keys_title_space('regions_cfg')
            ))
        else:
            await message.answer('Вы не подписаны на канал!\nt.me/*******')


@dp.message_handler(state=FSMOffer.channel_to)
async def get_channel_to(message: types.Message, state: FSMContext):
    if message.text.lower().replace(' ', '_') in get_json_keys('regions_cfg'):
        async with state.proxy() as data:
            data['channel_to'] = get_json_value('regions_cfg', message.text.lower().replace(' ', '_'))

        await message.answer('Теперь напишите название вашего товара')
        await FSMOffer.name.set()

    else:
        await message.answer("Такого региона не существует. Выберите из этого списка",
                             reply_markup=create_raw_reply_keyboard(
                                 get_json_keys_title_space('regions_cfg')))


@dp.message_handler(state=FSMOffer.name)
async def get_name(message: types.Message, state: FSMContext):
    m = message.text.lower()
    if m == 'да':
        await FSMOffer.condition.set()
        await message.answer('Теперь опишите состояние вашего товара, от 1 до 10')

    else:
        title = message.text.title()
        async with state.proxy() as data:
            data['name'] = title
        await message.answer(f'Название: ``` {title} ```||Отправьте название заново, чтобы изменить его||',
                             reply_markup=create_raw_reply_keyboard(['Да']),
                             parse_mode='MarkdownV2')


@dp.message_handler(state=FSMOffer.condition)
async def get_condition(message: types.Message, state: FSMContext):
    if message.text in [str(i) for i in range(1, 11)]:
        async with state.proxy() as data:
            data['condition'] = f'{"message.text"}/10'

        await message.answer('Введите цену товара')
        await FSMOffer.price.set()

    else:
        await message.reply('Введите цифру от 1 до 10')


@dp.message_handler(state=FSMOffer.price)
async def get_price(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Введите описание товара')
        await FSMOffer.description.set()

    elif message.text.isdigit():
        async with state.proxy() as data:
            data['price'] = message.text
        await message.reply(f'Цена: ```{data["price"]}₽```||Введите цену еще раз, чтобы редактировать||',
                            reply_markup=create_raw_reply_keyboard(['Да']),
                            parse_mode='MarkdownV2')

    else:
        await message.reply('Цена введена некорректно, попробуйте еще раз')


@dp.message_handler(state=FSMOffer.description)
async def get_description(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        global is_runned

        await FSMOffer.media.set()
        await state.update_data(media=[])
        await message.answer('Отправьте фотографии вашего товара')

        is_runned = False

    else:
        async with state.proxy() as data:
            data['description'] = message.text
        await message.reply(f'Описание:\n{data["description"]}\n\nНапишите описание еще раз, чтобы редактировать',
                            reply_markup=create_raw_reply_keyboard(['Да']))


@dp.message_handler(content_types=['any'], state=FSMOffer.media)
async def get_media(message: types.Message, state: FSMContext):
    await action(message, state)



'''

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
'''
