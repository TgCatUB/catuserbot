import contextlib
import sys

import userbot
from userbot import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("CatUserbot")

print(userbot.__copyright__)
print(f"Licensed under the terms of the {userbot.__license__}")

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
    print("============================================================")
    print("Yay your userbot is officially working.!!!")
    print(
        f"Congratulation, now type {cmdhr}alive to see message if catub is live\
        \nIf you need assistance, head to https://t.me/catuserbot_support"
    )
    print("============================================================")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


async def externalrepo():
    if Config.EXTERNAL_REPO:
        await install_externalrepo(
            Config.EXTERNAL_REPO, Config.EXTERNAL_REPOBRANCH, "xtraplugins"
        )
    if Config.BADCAT:
        await install_externalrepo(
            Config.BADCAT_REPO, Config.BADCAT_REPOBRANCH, "badcatext"
        )
    if Config.VCMODE:
        await install_externalrepo(Config.VC_REPO, Config.VC_REPOBRANCH, "catvc")


catub.loop.run_until_complete(startup_process())

catub.loop.run_until_complete(externalrepo())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        catub.run_until_disconnected()
else:
    catub.disconnect()
