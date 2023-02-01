from aiogram import Bot, Dispatcher
from creds.ApiKeys import tbot_api
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token=tbot_api)
dp = Dispatcher(bot, storage=storage)