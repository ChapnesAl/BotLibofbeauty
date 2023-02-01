from aiogram import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import admin, client  # , other
from handlers.knowledge_handlers import admin_knowl

async def on_startup(_):
    print('Бот ОНлайн')
    sqlite_db.sql_start()


async def on_shutdown(_):
    print('Бот ОФФлайн')




client.register_handler_client(dp)  # чтобы работало, client должен быть выше other
admin.register_handlers_admin(dp)
admin_knowl.register_handlers_admin(dp)

# other.register_handler_other(dp) # ставится последним


executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
print('Commands page <<<')
