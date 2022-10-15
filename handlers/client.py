from datetime import datetime

from aiogram.dispatcher import FSMContext

from Classes.MyClasses import StateToSend, States
from bot_dp import *
from database import sqlite_db
from func.client_func import command_in_text_func, text_confirmation_func, select_direction_func
from keyboard.client_kb import *


# handler for command "/start"
# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    start_message = "Привет! Я бот предназначенный для того, чтобы помочь тебе отправить заявку в канал, но так-же я " \
                    "имею несколько других функций.\n\nВот они:\nСписок комманд: /help\nОтправить сообщение админу: " \
                    "/send\nСоздать заявку на публикацию: /application\nВернуться к началу: /cancel\n\nПриятного " \
                    "пользования! "
    await message.answer(start_message, reply_markup=kb_all)


# handler for command "/help"
# @dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    help_message = "Вот список доступных комманд:\nСписок комманд: /help\nОтправить сообщение админу: /send\nСоздать " \
                   "заявку на публикацию: /application\nВернуться к началу: /cancel "
    await message.answer(help_message, reply_markup=kb_all)


# --------------------------------------------FSMContext----------------------------------------------------------------
@dp.message_handler(state="*", commands="cancel")
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Вам неоткуда выходить.", reply_markup=kb_help)
        return
    else:
        await state.finish()
    await message.answer("Завершено.", reply_markup=kb_help)


# ----------------------------------------FSMContext-send---------------------------------------------------------------
# handler for command "/send"
@dp.message_handler(commands="send", state=None)
async def command_send(message: types.Message):
    await message.answer('Всё, что вы напишите будет отправлено админу. Чтобы выйти введите /cancel',
                         reply_markup=types.ReplyKeyboardRemove())
    await StateToSend.TakeMessage.set()


# TakeMessage handler text
@dp.message_handler(content_types=['text'], state=StateToSend.TakeMessage)
async def text_application(message: types.Message):
    # Checking for the presence of a command in the application text
    if message.text.lower() == "стоп":
        await StateToSend.finish()
        await message.answer("Завершено.", reply_markup=kb_help)
    command_in_text = await command_in_text_func(message.text)
    if command_in_text:
        await message.answer("Вы не можете сейчас ввести комманду, повторите действие или введите /cancel.")
        await StateToSend.TakeMessage.set()
    elif not command_in_text:
        # saving the entered application text
        await bot.send_message(admin_id, message.from_user.username)
        await message.copy_to(admin_id)
        await message.answer("Отправлено!")


# TakeMessage handler all types
@dp.message_handler(
    content_types=['photo', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document', 'dice',
                   'animation', 'contact', 'sticker', 'location'], state=StateToSend.TakeMessage)
async def text_application(message: types.Message):
    # saving the entered application
    await bot.send_message(admin_id, message.from_user.username)
    await message.send_copy(admin_id)
    await message.answer("Отправлено!")


# ----------------------------------------FSMContext-application--------------------------------------------------------
# "/application" handler
@dp.message_handler(commands="application", state=None)
async def command_suggestion(message: types.Message):
    # StText setstate
    await States.Text.set()
    await message.answer("Введите текст вашего поста ниже:", reply_markup=types.ReplyKeyboardRemove())


# Text handler
@dp.message_handler(content_types=['text'], state=States.Text)
async def text_application(message: types.Message, state=FSMContext):
    # Checking for the presence of a command in the application text
    command_in_text = await command_in_text_func(message.text)
    if command_in_text:
        await message.answer("Вы не можете сейчас ввести комманду, повторите действие или введите /cancel.")
        await States.Text.set()
    else:
        # saving the entered application text and username
        async with state.proxy() as data:
            data['textfield'] = message.text
        await message.answer("Подтвердите ввод.", reply_markup=kb_text_confirmation)
        # StTextVer setstate
        await States.TextVerification.set()


# Text no text handler
@dp.message_handler(
    content_types=['photo', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document', 'dice',
                   'animation', 'contact', 'sticker', 'location'], state=States.Text)
async def not_a_text(message: types.Message):
    await message.answer("Это не текст, введите текст или /cancel")


# TextVerification handler
@dp.message_handler(content_types=['text'], state=States.TextVerification)
async def text_confirm(message: types.Message, state=FSMContext):
    # Text or PictureQuestion setstate
    await text_confirmation_func(message, message.text.lower())


# PictureQuestion handler
@dp.message_handler(content_types=['text'], state=States.PictureQuestion)
async def request_photo(message: types.Message, state: FSMContext):
    # Picture or Last setstate
    a_picture = await select_direction_func(message, message.text.lower())
    # Setting the value to None if there is no image
    if not a_picture:
        async with state.proxy() as data:
            data['photo'] = None


# Picture photo handler
@dp.message_handler(content_types=['photo'], state=States.Picture)
async def getting_photos(message: types.Message, state: FSMContext):
    # saving the photo file id
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    # Last setstate
    await message.answer('Чтобы сохранить заявку введите "Отправить"\nЧтобы отменить, введите /cancel',
                         reply_markup=kb_apply)
    await States.Last.set()


# Picture no picture handler
@dp.message_handler(
    content_types=['text', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document', 'dice',
                   'animation', 'contact', 'sticker', 'location'], state=States.Picture)
async def not_a_text(message: types.Message):
    await message.answer("Это не изображение, отправьте сжатую фотографию или введите /cancel")


# StLast handler, sending data to a table
@dp.message_handler(content_types=['text'], state=States.Last)
async def redirection_data(message: types.Message, state=FSMContext):
    await message.answer("Вы успешно отправили заявку на рассмотрение!", reply_markup=kb_help)
    async with state.proxy() as data:
        data['name'] = message.from_user.username
        dt = str(datetime.now()).replace(' ', '')
        dt = dt.replace(':', '')
        dt = dt.replace('.', '')
        data['datetime'] = dt
    # SQLite
    await sqlite_db.sql_add_application(state)
    await state.finish()


# ----------------------------------------------------------------------------------------------------------------------
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start', state=None)
    dp.register_message_handler(command_help, commands="help", state=None)
    dp.register_message_handler(command_send, commands="send", state=None)
