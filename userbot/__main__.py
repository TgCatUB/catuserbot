import sys

import userbot
from userbot import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .utils import (
    add_bot_to_logger_group,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("CatUserbot")

print(userbot.__copyright__)
print("Licensed under the terms of the " + userbot.__license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("Starting Userbot")
    catub.loop.run_until_complete(setup_bot())
    LOGS.info("TG Bot Startup Completed")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("Yay your userbot is officially working.!!!")
    print(
        f"Congratulation, now type {cmdhr}alive to see message if catub is live\
        \nIf you need assistance, head to https://t.me/catuserbot_support"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


catub.loop.run_until_complete(startup_process())


if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    try:
        catub.run_until_disconnected()
    except ConnectionError:
        pass
