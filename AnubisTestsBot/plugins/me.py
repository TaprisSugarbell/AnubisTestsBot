from aiogram import types, Bot
from .. import dp


@dp.message_handler(commands=["db"])
async def __dbse__(message: types.Message) -> None:
    print(message)
















