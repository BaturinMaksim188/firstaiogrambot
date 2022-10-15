from aiogram import types
from aiogram.dispatcher import FSMContext

from Classes.MyClasses import StateToAppend
from bot_dp import dp, bot, admin_id, channel_id
from database.sqlite_db import sql_read, sql_continue, on_delete_func
from func.admin_func import published_func
from keyboard.admin_kb import *
from keyboard.client_kb import kb_help


# -----------------------------------------States_on_command_/admin-----------------------------------------------------
# handler for command "/admin"
@dp.message_handler(commands=['admin'], state=None)
async def command_admin(message: types.Message):
    await StateToAppend.WelcomeState.set()
    await message.answer("Приветствую, вы можете посмотреть заявки.", reply_markup=kb_welcome)


# Handler for getting the path
@dp.message_handler(content_types=['text'], state=StateToAppend.WelcomeState)
async def view_or_exit(message: types.Message, state=FSMContext):
    if message.text.lower() == "посмотреть":
        read = await sql_read(state)
        if read == False:
            await message.answer("Заявок нет! Введите /help", reply_markup=kb_help)
            await state.finish()
        else:
            await message.answer("Что будем делать с этой заявкой?:", reply_markup=kb_cyclic)
            await published_func(state)
            await StateToAppend.CyclicState.set()
    elif message.text.lower() == "смотреть дальше":
        base_continue = await sql_continue(state)
        if base_continue == False:
            await message.answer("Заявки закончились! Введите /help", reply_markup=kb_help)
            await state.finish()
        else:
            await message.answer("Что будем делать с этой заявкой?:", reply_markup=kb_cyclic)
            await published_func(state)
            await StateToAppend.CyclicState.set()
    elif message.text.lower() == "выйти":
        await state.finish()
        await message.answer("Вы закончили обработку заявок!", reply_markup=kb_help)
    else:
        await message.reply("Я вас не понял, пожалуйста, повторите ввод.", reply_markup=kb_welcome)


# Handler for filtering unexpected messages
@dp.message_handler(content_types=['photo', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document',
                                   'dice', 'animation', 'contact', 'sticker', 'location'],
                    state=StateToAppend.WelcomeState)
async def view_or_exit_no_text(message: types.Message):
    await message.answer(
        'Пожалуйста, введите "Посмотреть" или "Выйти", воспользуйтесь клавиатурой или введите /cancel"')


# -----------------------------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['text'], state=StateToAppend.CyclicState)
async def actions_with_the_application(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "опубликовать":
            # If there is a photo in the post
            if data['pos'][1] != None:
                await bot.send_photo(channel_id, data['pos'][1], data['pos'][0])
                await on_delete_func(state)
                # Saving a position for deletion from the database after publication
                await StateToAppend.WelcomeState.set()
                await message.answer("Успешно опубликовано!", reply_markup=kb_check_processing)
            else:
                await bot.send_message(channel_id, data['pos'][0])
                await on_delete_func(state)
                await StateToAppend.WelcomeState.set()
                await message.answer("Успешно опубликовано!", reply_markup=kb_check_processing)

        elif message.text.lower() == "опции":
            await StateToAppend.ProcessingState.set()
            await message.reply("Вы хотите пропустить или удалить запись?", reply_markup=kb_processing)

        elif message.text.lower() == "выход":
            await StateToAppend.WelcomeState.set()
            await message.answer("Вы в приветственном (первом) состоянии, вы можете посмотреть заявки или выйти из "
                                 "него.", reply_markup=kb_welcome)
        else:
            await message.reply("Я вас не понимаю, воспользуйтесь клавиатурой или введите /cancel")


# Handler for filtering unexpected messages
@dp.message_handler(content_types=['photo', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document',
                                   'dice', 'animation', 'contact', 'sticker', 'location'],
                    state=StateToAppend.CyclicState)
async def actions_with_the_application_no_text(message: types.Message):
    await message.answer('Пожалуйста, воспользуйтесь клавиатурой или введите /cancel"', reply_markup=kb_cyclic)


# -----------------------------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['text'], state=StateToAppend.ProcessingState)
async def delete_or_skip_an_application(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "удалить":
            await on_delete_func(state)
            await StateToAppend.WelcomeState.set()
            await message.answer("Удалено!", reply_markup=kb_check_processing)
        elif message.text.lower() == "следующая":
            await StateToAppend.WelcomeState.set()
            await message.answer("Пропущено.", reply_markup=kb_check_processing)
        elif message.text.lower() == "назад":
            await StateToAppend.CyclicState.set()
            await message.answer("Возвращаемся...", reply_markup=kb_cyclic)
            await published_func(state)
        elif message.text.lower() == "выход":
            await StateToAppend.WelcomeState.set()
            await message.answer("Приветствую, вы можете посмотреть заявки.", reply_markup=kb_welcome)
        else:
            await message.reply("Я вас не понимаю, воспользуйтесь клавиатурой или введите /cancel",
                                reply_markup=kb_processing)


# Handler for filtering unexpected messages
@dp.message_handler(content_types=['photo', 'video', 'video_note', 'voice', 'poll', 'venue', 'audio', 'document',
                                   'dice', 'animation', 'contact', 'sticker', 'location'],
                    state=StateToAppend.CyclicState)
async def delete_or_skip_an_application_no_text(message: types.Message):
    await message.answer('Пожалуйста, воспользуйтесь клавиатурой или введите /cancel"', reply_markup=kb_processing)
