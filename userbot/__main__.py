from userbot import bot
from sys import argv
import importlib
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from config import Config
from userbot.utils import command
from pathlib import Path

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
        name = "userbot.plugins.{}".format(shortname.replace(".py", ""))
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.Config = Config
        mod.command = command
        # support for uniborg
        mod.borg = bot
        spec.loader.exec_module(mod)
        print("Successfully imported {}".format(f.name.replace("userbot/plugins/", "")))
import userbot._core
os.makedirs(Config.TEMP_DOWNLOAD_DIRECTORY)

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
