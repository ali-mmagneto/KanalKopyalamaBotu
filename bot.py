from pyrogram import Client, filters
from config import BOT_TOKEN, APP_ID, API_HASH, DEPO, userbot, DOWNLOAD_DIR
import random
import asyncio
from unidecode import unidecode
import time
import math 
PRGRS = {}

Bot = Client("RanmFilmBot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


import os
import time
import ffmpeg
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import asyncio
from subprocess import check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from PIL import Image

logging.getLogger("pyrogram").setLevel(logging.WARNING)


def ReadableTime(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def get_codec(filepath, channel="v:0"):
    output = check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            channel,
            "-show_entries",
            "stream=codec_name,codec_tag_string",
            "-of",
            "default=nokey=1:noprint_wrappers=1",
            filepath,
        ]
    )
    return output.decode("utf-8").split()




def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
      return None

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720


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


async def copy(bot, message, id, son_id, kanal_id, text1):
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
            await filmdongu(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

async def gizlicopy(bot, message, id, son_id, kanal_id, text1, sayi):
    try:
        if int(id) > int(son_id):
            await text1.edit("`İşlem Tamamlandı`")
            await sayi.edit("`İşlem Tamamlandı..`")
        else:
            await sayi.edit(f"`{id}. Mesaj Kopyalanıyor...`")
            film_kanal = await userbot.get_chat(chat_id=kanal_id)
            koruma = film_kanal.has_protected_content
            print(film_kanal.has_protected_content)
            if film_kanal.has_protected_content == True:
                chat_id = str(message.chat.id)
                film_kanal = await userbot.get_chat(chat_id=kanal_id)
                print(film_kanal)
                msg = await userbot.get_messages(kanal_id, id)
                caption = msg.caption
                start_time = time.time()
                
                if msg.video:
                    video = await userbot.download_media(
                        message = msg,
                        progress=progress_bar,
                        progress_args=("`İndiriliyor...`", text1, start_time))
                    duration = get_duration(video)
                    thumb_image_path = os.path.join(
                        DOWNLOAD_DIR,
                        chat_id,
                        chat_id + ".jpg"
                    )
                    if os.path.exists(thumb_image_path):
                        thumb = thumb_image_path
                    else:
                        thumb = get_thumbnail(video, './' + DOWNLOAD_DIR, duration / 4)
                    width, height = get_width_height(video)
                    file_size = os.stat(video).st_size
                    if file_size > 2093796556:
                        await userbot.send_video(
                            chat_id = DEPO,
                            progress = progress_bar, 
                            progress_args = (
                                'Dosyan Yükleniyor!',
                                text1,
                                start_time
                                ),
                            video = video,
                            caption = caption,
                            duration = duration,
                            thumb = thumb,
                            width = width,
                            height = height,
                            supports_streaming=True)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                    else:
                        await bot.send_video(
                            chat_id = DEPO,
                            progress = progress_bar, 
                            progress_args = (
                                'Dosyan Yükleniyor!',
                                text1,
                                start_time
                                ),
                            video = video,
                            caption = caption,
                            duration = duration,
                            thumb = thumb,
                            width = width,
                            height = height,
                            supports_streaming=True)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                elif msg.document:
                    video = await userbot.download_media(
                        message = msg,
                        progress=progress_bar,
                        progress_args=("`İndiriliyor...`", text1, start_time))
                    file_size = os.stat(video).st_size
                    if file_size > 2093796556:
                        await userbot.send_document(
                            chat_id = DEPO, 
                            document = video, 
                            caption = caption)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                    else:
                        await bot.send_document(
                            chat_id = DEPO, 
                            document = video, 
                            caption = caption)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                else:
                    await bot.send_message(message.chat.id, f"`{id}. Mesajın ne tür olduğunu bilmiyorum özür dilerim 😭😭`")
                    await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
            else:
                film_kanal = await userbot.get_chat(chat_id=kanal_id)
                print(film_kanal)
                await userbot.copy_message(
                    chat_id=DEPO, 
                    from_chat_id=kanal_id, 
                    message_id=int(id))
                await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
    except Exception as e:
        await message.reply_text(e)

async def filmdongu(bot, message, id, son_id, kanal_id, text1):
    try:
        id += 1
        await asyncio.sleep(5)
        await copy(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

async def filmdongug(bot, message, id, son_id, kanal_id, text1, sayi):
    try:
        id += 1
        await asyncio.sleep(5)
        await gizlicopy(bot, message, id, son_id, kanal_id, text1, sayi)
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
        sayi = await bot.send_message(message.chat.id, f"{kanal_id} {id} {son_id}")
        text1 = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongu(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

@Bot.on_message(filters.command("gizlifilm") & filters.private)
async def filmgg(bot, message):
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
        sayi = await bot.send_message(message.chat.id, f"@{kanal_id} {id} {son_id}")
        text1 = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
    except Exception as e:
        await message.reply_text(e)


@Bot.on_message(filters.incoming & filters.photo & filters.private)
async def save_photo(c, m):
    v = await m.reply_text("`Thumbnail Alıniyor..`", True)
    chat_id = str(m.from_user.id)
    path = os.path.join(
        DOWNLOAD_DIR,
        chat_id
    )
    thumb_image_path = os.path.join(
        path,
        chat_id + ".jpg"
    )

    downloaded_file_name = await m.download(
        file_name=thumb_image_path
    )
    Image.open(downloaded_file_name).convert(
        "RGB"
    ).save(downloaded_file_name)
    # ref: https://t.me/PyrogramChat/44663
    img = Image.open(downloaded_file_name)
    img.save(thumb_image_path, "JPEG")
    try:
        await v.edit_text("`Thumbnail Kaydedildi 😜`.")
    except Exception as e:
        print(f"#Error {e}")


@Bot.on_message(filters.incoming & filters.command(["delthumb"]))
async def delete_thumbnail(c, m):
    chat_id = str(m.from_user.id)
    path = os.path.join(
        DOWNLOAD_DIR,
        chat_id
    )
    thumb_image_path = os.path.join(
        path,
        chat_id + ".jpg"
    )
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await m.reply_text("`Thumbnail Silindi.`", quote=True)

Bot.run()
