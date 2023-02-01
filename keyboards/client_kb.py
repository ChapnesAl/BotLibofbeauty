from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Подборка знаний')
b2 = KeyboardButton('Рецепты')
b3 = KeyboardButton('Тренировки')
# b4 = KeyboardButton('Поделиться номером', request_location=True)
# b5 = KeyboardButton('Поделиться локацией', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)  # , one_time_keyboard=True) # 1ый параметр - меняет вид клавиатуры, второй параметр - прячет клавиатуры после нажатия

# kb_client.add(b1).add(b2).insert(b3)
# kb_client.row(b1, b2, b3)
# kb_client.row(b1, b2).add(b3) #.row(b4, b5)
kb_client.add(b1).add(b2).add(b3)
