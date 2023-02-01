from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    link = State()


# Получаем ID текущего модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    # await bot.send_message(message.from_user.id, 'К работе готов')  # without admin's keyboard
    await bot.send_message(message.from_user.id, 'К работе готов', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало диалога загрузки нового пункта меню / запуск Машины Состояний
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()  # бот переходит в ожидание получения фото
        await message.reply('Загрузи фото')


# Выход из машины состояния
# @dp.message_handler(state="*", commands='отмена')  # * в двойных кавычках = в каких бы состояниях из 5и бот не находился
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Готово, отменено')


# Ловим первый ответ
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:  # в словарь по ключу photo мы записываем картину по ее file id telegram
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()  # через метод next переводим бота в ожидание следующего ответа
        await message.reply('Введи название')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# Ловим третий
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Добавь цену')


# Ловим четвертый
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Добавь ссылку')


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.link)
async def load_link(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['link'] = message.text

        # without Data base
        # async with state.proxy() as data:
        #     await message.reply(str(data))  # возвращаем заполненный словарь
        # with Data Base
        await sqlite_db.sql_add_command(state)

        await state.finish()
        await message.answer('Всё добавлено')


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()  # take all datas from the table
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена; {ret[3]}')  # bot send some data
            await bot.send_message(message.from_user.id, text='^^^^', reply_markup=InlineKeyboardMarkup() # bot send inline button
                                   .add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрация хендлеров
def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_link, state=FSMAdmin.link)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
