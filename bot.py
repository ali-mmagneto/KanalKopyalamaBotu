from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO, STRING_SESSION
import random

Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("FilmBot", api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@Bot.on_message(filters.command("film") & filters.private)
async def film(bot, message):
    try:
        get_chat = await userbot.get_chat(FILM_DEPO)
        print(get_chat.title)
        message_id = random.randint(500, 1083)
        await userbot.copy_message(
            chat_id=message.chat.id, 
            from_chat_id=FILM_DEPO, 
            message_id=message_id)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "bir hata oluştu")
      
Bot.run()
userbot.start()
