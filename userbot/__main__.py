from userbot import bot
from sys import argv
import sys
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from var import Var
from userbot.utils import command, load_module
from userbot import LOAD_PLUG
from pathlib import Path
import userbot.utils

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
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
        print("Successfully (re)imported {}".format(f.name.replace("userbot/plugins/", "")))

import userbot._core

os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    self.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=api_config.APP_ID,
            api_hash=api_config.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
    bot.run_until_disconnected(await self.start(bot_token))
