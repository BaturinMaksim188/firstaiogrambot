from aiogram import types

from Classes.MyClasses import *
from keyboard.client_kb import *


# Checking for the presence of a command in the application text
async def command_in_text_func(n):
    if "/help" == n:
        return True
    elif "/start" == n:
        return True
    elif "/application" == n:
        return True
    elif "/send" == n:
        return True
    elif "/time" == n:
        return True
    elif "/admin" == n:
        return True
    else:
        return False


# Confirmation of the application text
async def text_confirmation_func(message, n):
    if "подтвердить" == n:
        await States.PictureQuestion.set()
        await message.answer("Подтверждено. Вы хотите приложить фотографию к будущему посту?",
                             reply_markup=kb_select_direction)
    elif "повторить" == n:
        await States.Text.set()
        await message.answer("Повторите ввод вашего текста.")
    else:
        await message.answer("Повторите ещё раз, я вас не расслышал :(", reply_markup=kb_text_confirmation)


# Receiving/rejecting a request to send a photo
async def select_direction_func(message, n):
    if "хочу!" == n:
        await message.answer("Отлично, тогда оправьте фотографию.", reply_markup=types.ReplyKeyboardRemove())
        await States.Picture.set()
        return True
    elif "нет..." == n:
        await message.answer('Чтобы сохранить заявку введите "Отправить"\nЧтобы отменить, введите /cancel',
                             reply_markup=kb_apply)
        await States.Last.set()
        return False
    else:
        await message.answer("Повторите ещё раз, я вас не расслышал :(", reply_markup=kb_select_direction)
