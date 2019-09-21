from userbot import bot
from sys import argv
import sys
import importlib
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from config import Config
from userbot.utils import command, load_module
from userbot import BAN_PLUG
import userbot.utils
from pathlib import Path
import logging
logging.basicConfig(level=logging.WARNING)

try:
    bot.start()
except PhoneNumberInvalidError:
    print("Phone Number you added was incorrect. Make sure to use your country code with your code")
    exit(1)

import glob
path = 'userbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path = Path(f.name)
        shortname = path.stem
        load_module(shortname.replace(".py", ""))
        print("Successfully (re)imported {}".format(f.name.replace("userbot/plugins/", "")))

impprt userbot._core

os.makedirs(Config.TEMP_DOWNLOAD_DIRECTORY)

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
