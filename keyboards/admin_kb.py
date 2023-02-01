from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# start keyboard buttons
button_product = KeyboardButton('Продукты')
button_recipes = KeyboardButton('Рецепты')
button_trains = KeyboardButton('Тренировки')
button_confirm_order = KeyboardButton('Подтвердить заказ')

button_case_admin_start = ReplyKeyboardMarkup(resize_keyboard=True).add(button_product) \
    .add(button_recipes).add(button_trains).add(button_confirm_order)


# after "start" buttons
button_add_product = KeyboardButton('Добавить')
button_del_product = KeyboardButton('Удалить')
button_back_to_start = KeyboardButton('Назад в разделы')

button_case_admin_actions = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_product).add(button_del_product)  \
                                                                    .add(button_back_to_start)

#  after "action" buttons
button_set = KeyboardButton("Добавить знание")
button_unique_set = KeyboardButton('Добавить уникальное')
button_back_to_action = KeyboardButton('Назад в действия')


button_case_admin_add_product = ReplyKeyboardMarkup(resize_keyboard=True).add(button_set) \
    .add(button_unique_set).add(button_back_to_action)

#  after "del" buttons
button_del_knowledge = KeyboardButton('Удалить знание')
button_del_unique = KeyboardButton('Удалить уникальное')
button_back_to_action = KeyboardButton('Назад в действия')


button_case_admin_del_product = ReplyKeyboardMarkup(resize_keyboard=True).add(button_del_knowledge).add(button_del_unique)  \
    .add(button_back_to_action)