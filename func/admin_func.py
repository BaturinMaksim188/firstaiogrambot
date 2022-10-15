from bot_dp import bot, channel_id, admin_id


async def published_func(state):
    async with state.proxy() as data:
        if data['pos'][1] != None:
            await bot.send_photo(admin_id, data['pos'][1], data['pos'][0])
            await bot.send_message(admin_id, f"Автор: {data['pos'][2]}")
        else:
            await bot.send_message(admin_id, data['pos'][0])
            await bot.send_message(admin_id, f"Автор: {data['pos'][2]}")


