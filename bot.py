from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, DEPO, userbot
import random
import asyncio
from unidecode import unidecode
import time

Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def progress_bar(current, total, text, message, start):

    now = time.time()
    diff = now-start
    if round(diff % 10) == 0 or current == total:
        percentage = current*100/total
        speed = current/diff
        elapsed_time = round(diff)*1000
        eta = round((total-current)/speed)*1000
        ett = eta + elapsed_time

        elapsed_time = TimeFormatter(elapsed_time)
        ett = TimeFormatter(ett)

        progress = "[{0}{1}] \n**İlerleme**: {2}%\n".format(
            ''.join(["●" for i in range(math.floor(percentage / 10))]),
            ''.join(["○" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))

        tmp = progress + "**Indirilen**: {0}/{1}\n**Hız**: `{2}`/s\n**Tahmini Süre**: `{3}`\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            ett if ett != '' else "0 s"
        )

        try :
            await message.edit(
                text = '{}'.format(tmp)
            )
        except:
            pass

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


async def copy(bot, message, id, son_id, kanal_id):
    try:
        if int(id) > int(son_id):
            await bot.send_message(message.chat.id, "`İşlem Tamamlandı`")
        else:
            film_kanal = await bot.get_chat(chat_id=kanal_id)
            print(film_kanal)
            await bot.copy_message(
                chat_id=DEPO, 
                from_chat_id=kanal_id, 
                message_id=int(id))
            await filmdongu(bot, message, id, son_id, kanal_id)
    except Exception as e:
        await message.reply_text(e)

async def gizlicopy(bot, message, id, son_id, kanal_id, mes):
    try:
        if int(id) > int(son_id):
            await bot.send_message(message.chat.id, "`İşlem Tamamlandı`")
        else:
            film_kanal = await userbot.get_chat(chat_id=kanal_id)
            print(film_kanal)
            msg = await userbot.get_messages(kanal_id, id)
            caption = msg.caption
            start_time = time.time()
            video = await userbot.download_media(
                message = msg,
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", text, start_time))
            await userbot.send_video(
                chat_id = DEPO,
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    text,
                    start_time
                    ),
                video = video,
                caption = caption,
                supports_streaming=True)
            await filmdongu(bot, message, id, son_id, kanal_id, text)
    except Exception as e:
        await message.reply_text(e)

async def filmdongu(bot, message, id, son_id, kanal_id, text):
    try:
        id += 1
        await asyncio.sleep(5)
        await gizlicopy(bot, message, id, son_id, kanal_id, text)
    except Exception as e:
        await message.reply_text(e)

@Bot.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        text = unidecode(message.text).split()
        if len(text) < 4:
            await message.reply_text("Hatalı Kullanım")
            return
        kanal_id = str(text[1])
        id = int(text[2])
        son_id = text[3]
        print(kanal_id) 
        print(id) 
        print(son_id) 
        await message.reply_text(f"@{kanal_id} {id} {son_id}")
        text = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongu(bot, message, id, son_id, kanal_id, text)
    except Exception as e:
        await message.reply_text(e)

@Bot.on_message(filters.command("gizlifilm") & filters.private)
async def filmg(bot, message):
    try:
        text = unidecode(message.text).split()
        if len(text) < 4:
            await message.reply_text("Hatalı Kullanım")
            return
        kanal_id = str(text[1])
        id = int(text[2])
        son_id = text[3]
        print(kanal_id) 
        print(id) 
        print(son_id) 
        await message.reply_text(f"@{kanal_id} {id} {son_id}")
        text = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongu(bot, message, id, son_id, kanal_id, text)
    except Exception as e:
        await message.reply_text(e)
    
Bot.run()
