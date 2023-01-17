import re
import os
from os import environ

BOT_TOKEN = environ.get("BOT_TOKEN", "")
PRE_LOG = environ.get("PRE_LOG", "") 
APP_ID = int(environ.get("APP_ID", 1234))
API_HASH = environ.get("API_HASH", "")
