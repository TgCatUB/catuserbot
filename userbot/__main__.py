from userbot import bot
from sys import argv
import sys
import importlib
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from config import Config
from userbot.utils import command
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

def load_module(shortname):
    name = "userbot.plugins.{}".format(shortname)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.bot = bot
    mod.Config = Config
    mod.command = command
    # support for uniborg
    sys.modules["uniborg.util"] = userbot.utils
    mod.borg = bot
    # support for paperplaneextended
    sys.modules["userbot.events"] = userbot.utils
    spec.loader.exec_module(mod)

import glob
import userbot._core
path = 'userbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path = Path(f.name)
        shortname = path.stem
        load_module(shortname.replace(".py", ""))
        print("Successfully (re)imported {}".format(f.name.replace("userbot/plugins/", "")))

os.makedirs(Config.TEMP_DOWNLOAD_DIRECTORY)

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
