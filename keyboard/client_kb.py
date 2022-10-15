from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Buttons on start_message
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/send')
b3 = KeyboardButton('/application')
b4 = KeyboardButton('/cancel')
kb_all = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_all.add(b1).add(b2, b3).add(b4)

# Button on help_message
b_help = KeyboardButton('/help')
kb_help = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_help.add(b_help)

# Buttons on verification text
confirm = KeyboardButton('Подтвердить')
dont_confirm = KeyboardButton('Повторить')
kb_text_confirmation = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_text_confirmation.add(confirm).add(dont_confirm)

# Buttons on PictureQuestion
want = KeyboardButton('Хочу!')
dont_want = KeyboardButton('Нет...')
kb_select_direction = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_select_direction.add(want).add(dont_want)

# Buttons on application confirm
send = KeyboardButton('Отправить')
dont_send = KeyboardButton('/cancel')
kb_apply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_apply.add(send).add(dont_send)

# Button "/cancel" on send
cancel = KeyboardButton('Стоп')
kb_send = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
