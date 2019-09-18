from userbot import bot
from sys import argv
import importlib
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot.plugins import ALL_MODULES

try:
    bot.start()
except PhoneNumberInvalidError:
    print("Phone Number you added was incorrect. Make sure to use your country code with your code")
    exit(1)

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.plugins." + module_name)

print("Yay your userbot is officially working.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
