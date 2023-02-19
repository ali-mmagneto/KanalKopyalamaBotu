import re
import os
from os import environ
import pyrogram
from pyrogram import Client

BOT_TOKEN = environ.get("BOT_TOKEN", "") 
DEPO = environ.get("DEPO", "")
APP_ID = int(environ.get("APP_ID", 1234))
API_HASH = environ.get("API_HASH", "")
