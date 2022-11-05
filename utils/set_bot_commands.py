from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Ознакомиться с функционалом бота"),
            types.BotCommand("offer", "Предложить объявление")
        ]
    )
