import sqlite3 as sql
from aiogram.dispatcher import FSMContext
from bot_dp import bot, admin_id


# open/create sql table
def sql_start():
    global base, cursor
    base = sql.connect("applications.db")
    cursor = base.cursor()
    if base:
        print("DB connected")
    base.execute('CREATE TABLE IF NOT EXISTS applications(textfield TEXT, photo TEXT, name TEXT, datetime TEXT)')
    base.commit()


# sql add an application
async def sql_add_application(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO applications VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Getting the first record from the database and returning False if it is missing
async def sql_read(state=FSMContext):
    cursor.execute('SELECT * FROM applications')
    async with state.proxy() as data:
        data['pos'] = cursor.fetchone()
        data['score'] = 1
        if data['pos'] != None:
            await bot.send_message(admin_id, f"На данный момент их {len(cursor.fetchall())+1}.")
        else:
            return False


# Getting the next record from the database and returning False if it is missing
async def sql_continue(state=FSMContext):
    cursor.execute('SELECT * FROM applications')
    async with state.proxy() as data:
        for i in range(data['score']):
            cursor.fetchone()
        score = data['score']
        del data['score']
        data['score'] = (score + 1)
        del data['pos']
        data['pos'] = cursor.fetchone()
        if data['pos'] != None:
            return True
        else:
            return False


# Deleting a record from the database and moving the index up
async def on_delete_func(state):
    async with state.proxy() as data:
        cursor.execute('DELETE from applications where datetime = (?)', (data['pos'][3],))
        score = data['score']
        del data['score']
        data['score'] = (score - 1)
        base.commit()