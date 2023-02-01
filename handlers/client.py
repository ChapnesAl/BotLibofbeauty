from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.dispatcher.filters import Text


# @dp.message_handler(commands=['start', 'help'])
async def base_commands(message: types.Message):
    try:
        await bot.send_message(message.chat.id, '<b>Hello</b>', parse_mode='html',
                               reply_markup=kb_client)  # добавлен параметр который поднимает свою клавиатуру
        await message.delete()
    except:
        await message.reply('Напишите боту \nhttps://t.me/FirstStock_bot')


# @dp.message_handler(commands=['Список моделей']) # у бота пишется с /
async def knowledge_general(message: types.Message):
    # await bot.send_message(message.chat.id, 'Список моделей') # old example
    await sqlite_db.sql_read(message)


# @dp.message_handler(commands=['Полезные материалы'])
async def recipes_general(message: types.Message):
    await bot.send_message(message.chat.id, 'Видео: Статьи: Новости:')


async def trains_general(message: types.Message):
    await bot.send_message(message.chat.id, 'Напишите ваш вопрос:',
                           reply_markup=ReplyKeyboardRemove())  # последний параметр и аргумент убирают свою клавиатуру


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(base_commands, commands=['start', 'help'])
    dp.register_message_handler(knowledge_general, Text(equals='Подборка знаний'))
    dp.register_message_handler(recipes_general, Text(equals='Рецепты'))
    dp.register_message_handler(trains_general, Text(equals='Тренировки'))
