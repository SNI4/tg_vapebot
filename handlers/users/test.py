import asyncio
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import json
class FSMTest(StatesGroup):

    media = State()

@dp.message_handler(commands=['load'])
async def test(message: types.Message, state: FSMContext):
    await FSMTest.media.set()
    await state.update_data(media=[])
    await message.reply('wait for photo(s)...')

@dp.message_handler(content_types=['any'], state=FSMTest.media)
async def load(message: types.Message, state: FSMContext):

    if message.text != 'loaded':
        async with state.proxy() as data:
            data['media'].append(message.photo[-1].file_id)


    elif message.text == 'loaded':
        await message.reply('finished')
        async with state.proxy() as data:

            group = types.MediaGroup()
            async for photo_id in data['media']:
                group.attach_photo(photo_id)
            await bot.send_media_group(message.chat.id, group)

        await state.finish()

