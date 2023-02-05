from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO
import random


Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def copy(bot, message, message_id, text):
    try:
        get_chat = await bot.get_chat(FILM_DEPO)
        print(get_chat.title)
        await bot.copy_message(
            chat_id=message.chat.id, 
            from_chat_id=FILM_DEPO, 
            message_id=int(message_id))
        await text.delete()
        await filmdongu(bot, message)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "bir hata oluştu")


async def filmdongu(bot, message):
    try:
        message_id = [153] 
        text = await bot.send_message(
            chat_id=message.chat.id,
            text="işlem Yapıyom")
        message_id.append(message)
        await copy(bot, message, message_id, text)
    except Exception as e:
        print(e)

@Bot.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        await filmdongu(bot, message)
    except Exception as e:
        print(e)
   
    
Bot.run()

