from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from data_base import sqlite_db
from keyboards import admin_kb


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    link = State()
    price = State()


type_of_product = None


async def back_to_start(message: types.Message):
    if message.from_user.id == message.from_user.id:
        await message.reply('Выберите раздел:', reply_markup=admin_kb.button_case_admin_start)


async def add_kind_products(message: types.Message):
    if message.from_user.id == message.from_user.id:
        await message.reply('Выберите тип ниже:', reply_markup=admin_kb.button_case_admin_add_product)


async def back_to_actions(message: types.Message):
    if message.from_user.id == message.from_user.id:
        await message.reply('Выберите действие ниже:', reply_markup=admin_kb.button_case_admin_actions)


async def del_kind_products(message: types.Message):
    if message.from_user.id == message.from_user.id:
        await message.reply('Выберите тип ниже:', reply_markup=admin_kb.button_case_admin_del_product)


# Начало диалога загрузки нового пункта меню / запуск Машины Состояний
async def add_knowledge(message: types.Message):
    global type_of_product
    type_of_product = "not unique"
    if message.from_user.id == message.from_user.id:
        await FSMAdmin.photo.set()  # бот переходит в ожидание получения фото
        await message.reply('Загрузи фото')


async def add_unique_product(message: types.Message):
    global type_of_product
    type_of_product = "unique"
    if message.from_user.id == message.from_user.id:
        await FSMAdmin.photo.set()  # бот переходит в ожидание получения фото
        await message.reply('Загрузи фото')


# Выход из машины состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Готово, отменено')


# Ловим первый ответ
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == message.from_user.id:
        async with state.proxy() as data:  # в словарь по ключу photo мы записываем картину по ее file id telegram
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()  # через метод next переводим бота в ожидание следующего ответа
        await message.reply('Введи название')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == message.from_user.id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# Ловим третий
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == message.from_user.id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Добавь ссылку')


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.link)
async def load_link(message: types.Message, state: FSMContext):
    if type_of_product == "unique":
        if message.from_user.id == message.from_user.id:
            async with state.proxy() as data:
                data['link'] = message.text
            await FSMAdmin.next()
            await message.reply('Добавь цену')
    else:
        if message.from_user.id == message.from_user.id:
            async with state.proxy() as data:
                data['link'] = message.text
            # without Data base
            # async with state.proxy() as data:
            #     await message.reply(str(data))  # возвращаем заполненный словарь
            # with Data Base
            await sqlite_db.sql_add_free(state)

            await state.finish()
            await message.answer('Всё добавлено')


# Ловим четвертый
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == message.from_user.id:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        # without Data base
        # async with state.proxy() as data:
        #     await message.reply(str(data))  # возвращаем заполненный словарь
        # with Data Base
        await sqlite_db.sql_add_unique(state)
        await state.finish()
        await message.answer('Всё добавлено')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_knowledge, Text(equals='Добавить знание'), state=None)
    dp.register_message_handler(add_unique_product, Text(equals='Добавить уникальное'), state=None)
    dp.register_message_handler(del_kind_products, Text(equals='Удалить продукт'), state=None)
    dp.register_message_handler(add_kind_products, Text(equals='Добавить'))
    dp.register_message_handler(del_kind_products, Text(equals='Удалить'))
    dp.register_message_handler(back_to_actions, Text(equals='Назад в действия'))
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_link, state=FSMAdmin.link)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')