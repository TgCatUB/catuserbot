import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

import userbot
from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .helpers.utils import install_pip
from .sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from .sql_helper.globals import gvarstatus,addgvar
from .utils import load_module, verifyLoggerGroup, setup_bot, startupmessage, add_bot_to_logger_group, load_plugins

LOGS = logging.getLogger("CatUserbot")

print(userbot.__copyright__)
print("Licensed under the terms of the " + userbot.__license__)

cmdhr = Config.COMMAND_HAND_LER


try:
    LOGS.info("Starting Userbot")
    catub.loop.run_until_complete(setup_bot())
    LOGS.info("TG Bot Startup Completed")
except Exception as e:
    LOGS.error(f"{str(e)}")
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
    await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()

catub.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    catub.run_until_disconnected()
