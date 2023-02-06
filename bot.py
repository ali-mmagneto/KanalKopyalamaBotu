from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO, DEPO, SON_MSG_ID, ILK_MSG_ID, STRING_SESSION
import random
import asyncio

Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("RanmuserBot", api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION)

async def copy(bot, message, id):
    try:
        if id > SON_MSG_ID:
            await bot.send_message(message.chat.id, "`İşlem Tamamlandı`")
        else:
            film_kanal = await userbot.get_chat(chat_id=FILM_DEPO)
            print(film_kanal)
            await userbot.copy_message(
                chat_id=DEPO, 
                from_chat_id=FILM_DEPO, 
                message_id=id)
            await filmdongu(bot, message, id)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, f"bir hata oluştu `{e}`")

async def filmdongu(bot, message, id):
    try:
        id += 1
        await asyncio.sleep(5)
        await copy(bot, message, id)
    except Exception as e:
        print(e)

@Bot.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        id = ILK_MSG_ID
        text = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongu(bot, message, id)
    except Exception as e:
        print(e)
    
Bot.run()
userbot.start()
