import logging

from aiogram import Bot, Dispatcher, Router
from tortoise import Tortoise
from helper.load_plugins import load_modules
from __vars__ import BOT_TOKEN

PACKAGE = __package__

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
form_router = Router()
dp = Dispatcher()


async def connect(db_url: str, models: list):
    logging.info("create database")
    await Tortoise.init(
        db_url=db_url,
        modules={'models': models}
    )
    logging.info("Generate the schema")
    await Tortoise.generate_schemas()

