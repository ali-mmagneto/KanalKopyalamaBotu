import re
import os
from os import environ
import pyrogram
from pyrogram import Client

BOT_TOKEN = environ.get("BOT_TOKEN", "")
STRING_SESSION = environ.get("STRING_SESSION", "") 
DEPO = environ.get("DEPO", "")
APP_ID = int(environ.get("APP_ID", 1234))
API_HASH = environ.get("API_HASH", "")
userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
userbot.start()
