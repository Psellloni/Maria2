import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from main import DataHandler as dh
from config import tg_token

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здравствуйте, {hbold(message.from_user.full_name)}!")

@dp.message()
async def echo_handler(message: types.Message) -> None:
    text = message.text
    rep = dh.brain(text.lower())

    await message.answer(text=rep)

async def main() -> None:
    bot = Bot(tg_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())