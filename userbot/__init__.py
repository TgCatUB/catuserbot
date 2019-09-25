import logging
import os
import sys
from pathlib import Path
from telethon.sessions import StringSession
from telethon import TelegramClient

from config import Var

os.system("pip install --upgrade pip")
if Var.STRING_SESSION:
    session_name = str(Var.STRING_SESSION)
    bot = TelegramClient(StringSession(session_name), Config.APP_ID, Config.API_HASH)
else:
    session_name = "startup"
    bot = TelegramClient(session_name, Config.APP_ID, Config.API_HASH)


CMD_LIST = {}
# for later purposes
CMD_HELP = {}
INT_PLUG = ""
LOAD_PLUG = {}
BOTLOG = os.environ.get("BOTLOG", False)
BOTLOG_CHATID = os.environ.get("BOTLOG_CHATID", None)
