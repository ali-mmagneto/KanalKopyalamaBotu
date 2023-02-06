import re
import os
from os import environ
import pyrogram
from pyrogram import Client

BOT_TOKEN = environ.get("BOT_TOKEN", "")
STRING_SESSION = environ.get("STRING_SESSION", "")
FILM_DEPO = environ.get("FILM_DEPO", "") 
DEPO = environ.get("DEPO", "")
APP_ID = int(environ.get("APP_ID", 1234))
API_HASH = environ.get("API_HASH", "")
SON_MSG_ID = int(environ.get("SON_MSG_ID", ""))
ILK_MSG_ID = int(environ.get("ILK_MSG_ID", ""))
userbot = Client("RanmuserBot", api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION)
userbot.start()
