from bot_dp import *
from keyboard.client_kb import *

# handler handling all random messages
async def blank_message(message: types.Message):
    answer = "Я не могу с вами разговаривать без разрешения, он наблюдает..\nЛучше нажмите сюда: /help"
    await message.answer(answer, reply_markup=kb_help)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(blank_message, content_types=['text', 'photo', 'video', 'video_note', 'voice', 'poll',
                                                              'venue', 'audio', 'document', 'dice', 'animation',
                                                              'contact', 'sticker', 'location'], state=None)
