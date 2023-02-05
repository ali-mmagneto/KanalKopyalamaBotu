from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO
import random

Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def copy(bot, message):
    try:
        get_chat = await bot.get_chat(FILM_DEPO)
        print(get_chat.title)
        message_id = random.randint(153, 3554)
        await bot.copy_message(
            chat_id=message.chat.id, 
            from_chat_id=FILM_DEPO, 
            message_id=message_id)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "bir hata oluştu")


@Bot.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text="işlem Yapıyom")
        id=350
        await copy(bot, message)
    except Exception as e:
        print(e)
   
    
Bot.run()

