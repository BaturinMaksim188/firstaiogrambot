import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

storage = MemoryStorage()

admin_id = !!!!!!!!!!!!!PUTYOURADMINIDHERE!!!!!!!!!!!!!!!!!
channel_id = !!!!!!!!!!!!!PUTYOURCHANNELIDHERE!!!!!!!!!!!!!!!!!!

# Токен бота
bot = Bot(token='!!!!!!!!!!!!!!!!!!!PUTYOURTOKENHERE!!!!!!!!!!!!!!!!!', parse_mode=types.ParseMode.HTML)
# Диспетчер
dp = Dispatcher(bot, storage=storage)
# Устанавливаем логгирование
dp.middleware.setup(LoggingMiddleware())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
