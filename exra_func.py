from aiogram.utils import executor
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import Dispatcher
from creds.ApiKeys import tbot_api



bot = Bot(token=tbot_api)
dp = Dispatcher(bot)


# if bot finds this value it does what to need
@dp.message_handler(lambda message: 'status' in message.text)
async def ask_status(message: types.Message):
    await message.answer('get status')

# algorithm gets data after some value
@dp.message_handler(lambda message: message.text.startswith('name'))
async def ask_status(message: types.Message):
    await message.answer(message.text[5:])



# выводит ответ если бот не находит ее + должна стоять после других команд
@dp.message_handler()
async def empry(message: types.Message):
    await message.answer("Нет такой команды, но есть такие: (условное перечисление)")
    await message.delete()

executor.start_polling(dp, skip_updates=True)