from startup import bot
from sys import argv
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

try:
    bot.start()
except PhoneNumberInvalidError:
    print("Phone Number you added was incorrect. Make sure to use your country code with your code")
    exit(1)

from userbot.plugins import *

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
