from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
from creds.ApiKeys import tbot_api
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

bot = Bot(token=tbot_api)
dp = Dispatcher(bot)

answ = dict()

# inline button with link
urlkb = InlineKeyboardMarkup(row_width=2)  # one button in row
urlButton = InlineKeyboardButton(text='Link', url='https://www.youtube.com/watch?v=gpCIfQUbYlY')
urlButton2 = InlineKeyboardButton(text='Link2', url='https://www.youtube.com/watch?v=m0ZRms4p7fc')
three_buttons = [InlineKeyboardButton(text='Link3', url='https://www.youtube.com/watch?v=m0ZRms4p7fc'),
                 InlineKeyboardButton(text='Link4', url='https://www.youtube.com/watch?v=m0ZRms4p7fc'),
                 InlineKeyboardButton(text='Link5', url='https://www.youtube.com/watch?v=m0ZRms4p7fc')]
urlkb.add(urlButton, urlButton2).row(*three_buttons).insert(InlineKeyboardButton(text='Link6', url='https://www.youtube.com/watch?v=m0ZRms4p7fc'))
# ^ method 'insert' adds button if there is a place for it

@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    await message.answer('Links: ', reply_markup=urlkb)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Push me', callback_data='www'))


@dp.message_handler(commands='test')
async def url_command(message: types.Message):
    await message.answer('inline button', reply_markup=inkb)

# handler couch callback in inline button
@dp.callback_query_handler(text='www')
async def www_call(callback: types.CallbackQuery):
    # await callback.answer('inline button was pushing')  # короткое упоминание в центре экрана
    # await callback.message.answer('inline button was pushing')
    # await callback.answer('button was pushing')  # тут мы подтверждаем что все бот по строке выше получил
    await callback.answer('button was pushing', show_alert=True)  # show alert is the parameter which shows additional window in the middle of screen




voting = InlineKeyboardMarkup(row_width=2)  # one button in row
like = InlineKeyboardButton(text='Like', callback_data='like_+1')
dislike = InlineKeyboardButton(text='Dislike', callback_data='like_-1')


voting.add(like).add(dislike)

@dp.message_handler(commands='voting')
async def url_command(message: types.Message):
    await message.answer('chose you option ', reply_markup=voting)


@dp.callback_query_handler(Text(startswith='like_'))  # "Text" filter, or we can use the filter 'lambda'
async def www_call(callback: types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:  # if user voted, he can't repeat this action
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('You had voting')
    else:
        await callback.answer('You voted before', show_alert=True)



executor.start_polling(dp, skip_updates=True)
