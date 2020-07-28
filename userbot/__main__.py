from userbot import bot
from sys import argv
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon import TelegramClient
from var import Var
from userbot.utils import load_module
from userbot import LOAD_PLUG, LOGS
from pathlib import Path
import telethon.utils
import userbot._core
import glob

async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me() 
    bot.uid = telethon.utils.get_peer_id(bot.me)

  
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None 
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        LOGS.info("Initiating Inline Bot")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        LOGS.info("Initialisation finished with no errors")
        LOGS.info("Starting Userbot")
        bot.loop.run_until_complete(add_bot(Var.TG_BOT_USER_NAME_BF_HER))
        LOGS.info("Startup Completed")
    else:
        bot.start()
    
path = 'userbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
        
LOGS.info("Yay your userbot is officially working.!!!")
LOGS.info("Congratulation, now type .alive to see message if bot is live\n"
          "If you need assistance, head to https://t.me/catuserbot_support")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()  
