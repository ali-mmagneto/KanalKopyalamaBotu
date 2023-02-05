from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO, DEPO
import random


Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def copy(bot, message, text, id):
    try:
        get_chat = await bot.get_chat(FILM_DEPO)
        print(get_chat.title)
        await bot.copy_message(
            chat_id=DEPO, 
            from_chat_id=FILM_DEPO, 
            message_id=id)
        await text.delete()
        await filmdongu(bot, message, id)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, f"bir hata oluştu `{e}`")

async def filmdongu(bot, message, id):
    try:
        id += 1
        text = await bot.send_message(
            chat_id=message.chat.id,
            text="işlem Yapıyom")
        await copy(bot, message, text, id)
    except Exception as e:
        print(e)

@Bot.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        id = 152
        await filmdongu(bot, message, id)
    except Exception as e:
        print(e)
   
    
Bot.run()

