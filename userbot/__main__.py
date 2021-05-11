import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import functions

import userbot
from userbot.Config import Config
from userbot.core.logger import logging
from userbot.core.session import catub
from userbot.utils import load_module

LOGS = logging.getLogger(__name__)

print(userbot.__copyright__)
print("Licensed under the terms of the " + userbot.__license__)


async def testing_bot():
    try:
        await catub.connect()
        config = await catub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == catub.session.server_address:
                if catub.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {catub.session.dc_id}"
                        f" to {option.id}"
                    )
                catub.session.set_dc(option.id, option.ip_address, option.port)
                catub.session.save()
                break
        await catub.start(bot_token=Config.TG_BOT_USERNAME)
        catub.me = await catub.get_me()
        catub.uid = telethon.utils.get_peer_id(catub.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    try:
        LOGS.info("Starting Userbot")
        catub.loop.run_until_complete(testing_bot())
        LOGS.info("Startup Completed")
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


path = "userbot/plugins/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                load_module(shortname.replace(".py", ""))
            else:
                os.remove(Path(f"userbot/plugins/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"userbot/plugins/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")


print("Yay your userbot is officially working.!!!")
print(
    "Congratulation, now type .alive to see message if catub is live\
      \nIf you need assistance, head to https://t.me/catuserbot_support"
)


async def startupmessage():
    try:
        if Config.PRIVATE_GROUP_BOT_API_ID != 0:
            await catub.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID,
                "**Congratulation, now type .alive to see message if catub is live\
        \nIf you need assistance, **head to https://t.me/catuserbot_support",
                link_preview=False,
            )
    except Exception as e:
        LOGS.info(str(e))


catub.loop.create_task(startupmessage())

if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    catub.run_until_disconnected()
