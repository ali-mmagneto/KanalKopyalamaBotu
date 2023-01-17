from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, FILM_DEPO
import random

Bot = Client("RandomFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

message_id = random.randint(4, 1456)

@Bot.on_message(filters.command("film") & filters.private)
async def film(bot, message):
    try:
        await bot.copy_message(
            chat_id=chat_id, 
            from_chat_id=FILM_DEPO, 
            message_id=message_id)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "bir hata oluştu")
      
bot.run()
