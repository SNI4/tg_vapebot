import asyncio

from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import json

class FSMTest(StatesGroup):
    media = State()

@dp.message_handler(commands=['load'], state=None)
async def test(message: types.Message):
    await FSMTest.media.set()
    await message.reply('wait for photo(s)...')

@dp.message_handler(content_types=['any'], state=FSMTest)
async def load(message: types.Message, state=FSMTest):
    med = json.loads(message.as_json())
    media_list = []
    # https://ru.stackoverflow.com/questions/1198860/Сохранение-всех-фото-из-альбома-без-message-handlercontent-types-photo/1202083#1202083
    if 'media_group_id' in med:
        for pic in med['photo']:
            pic_id = pic['file_id']
            media_list.append(pic_id) if pic_id not in media_list else ...
            await message.reply(' ; '.join(media_list))
            await state.finish()
    else:
        await message.reply(message.photo[-1].file_id)
        await state.finish()
