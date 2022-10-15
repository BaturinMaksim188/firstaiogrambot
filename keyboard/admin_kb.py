from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# kb_welcome
view = KeyboardButton('Посмотреть')
dont_view = KeyboardButton('Выйти')
kb_welcome = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_welcome.add(view).add(dont_view)


# kb_cyclic
post = KeyboardButton('Опубликовать')
skip = KeyboardButton('Опции')
out_of_CyclicState = KeyboardButton('Выход')
kb_cyclic = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cyclic.add(post, skip).add(out_of_CyclicState)


# kb_processing
delete_position = KeyboardButton('Удалить')
next_position = KeyboardButton('Следующая')
previous_position = KeyboardButton('Назад')
out_of_ProcessingState = KeyboardButton('Выход')
kb_processing = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_processing.add(delete_position, next_position).add(previous_position).add(out_of_ProcessingState)

# kb_check_processing
next_post = KeyboardButton('Смотреть дальше')
not_next_post = KeyboardButton('Выйти')
kb_check_processing = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_check_processing.add(next_post).add(not_next_post)