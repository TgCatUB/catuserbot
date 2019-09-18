from userbot import bot
from sys import argv
import importlib
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

try:
    bot.start()
except PhoneNumberInvalidError:
    print("Phone Number you added was incorrect. Make sure to use your country code with your code")
    exit(1)

import glob
import errno
path = 'userbot/modules/*.py'
files = glob.glob(path)
for name in files:
    try:
        with open(name) as f:
            imported_module = importlib.import_module(f)
            print(f"Successfully imported {f}")
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
