import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('free_products.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    base.execute(
        'CREATE TABLE IF NOT EXISTS free_prod(img TEXT, name TEXT PRIMARY KEY, description TEXT, link TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS unique_prod(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT, link TEXT)')
    base.commit()


async def sql_add_free(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO free_prod VALUES ( ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_add_unique(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO unique_prod VALUES ( ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM free_prod').fetchall():
        await bot.send_photo(message.from_user.id, ret[0],
                             f' {ret[1]}\n Описание: {ret[2]}\n Скачать по ссылке: {ret[3]}') # \n Ссылка {ret[4]}')



