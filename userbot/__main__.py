import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

import userbot
from userbot import BOTLOG, BOTLOG_CHATID

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .helpers.utils import install_pip
from .sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from .sql_helper.globals import gvarstatus
from .utils import load_module

LOGS = logging.getLogger("CatUserbot")

print(userbot.__copyright__)
print("Licensed under the terms of the " + userbot.__license__)

cmdhr = Config.COMMAND_HAND_LER


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
        catub.uid = catub.tgbot.uid = utils.get_peer_id(catub.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(catub.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


def verifyLoggerGroup():
    if BOTLOG:
        try:
            entity = catub.loop.run_until_complete(catub.get_entity(BOTLOG_CHATID))
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified Logger group."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified Logger group."
                    )
        except ValueError:
            LOGS.error("Logger group ID cannot be found. " "Make sure it's correct.")
        except TypeError:
            LOGS.error("Logger group ID is unsupported. " "Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the logger group.\n"
                + str(e)
            )
        try:
            entity = catub.loop.run_until_complete(
                catub.get_entity(Config.PM_LOGGER_GROUP_ID)
            )
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified Pm logger group."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified Pm Logger group."
                    )
        except ValueError:
            LOGS.error("Pm Logger group ID cannot be found. " "Make sure it's correct.")
        except TypeError:
            LOGS.error("Pm Logger group ID is unsupported. " "Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the Pm logger group.\n"
                + str(e)
            )
    else:
        LOGS.info(
            "You haven't set the PRIVATE_GROUP_BOT_API_ID in vars please set it for proper functioning of userbot."
        )


def add_bot_to_logger_group():
    bot_details = catub.loop.run_until_complete(catub.tgbot.get_me())
    Config.TG_BOT_USERNAME = f"@{bot_details.username}"
    try:
        catub.loop.run_until_complete(
            catub(
                functions.messages.AddChatUserRequest(
                    chat_id=BOTLOG_CHATID,
                    user_id=bot_details.username,
                    fwd_limit=1000000,
                )
            )
        )
        catub.loop.run_until_complete(
            catub(
                functions.messages.AddChatUserRequest(
                    chat_id=Config.PM_LOGGER_GROUP_ID,
                    user_id=bot_details.username,
                    fwd_limit=1000000,
                )
            )
        )
    except BaseException:
        try:
            catub.loop.run_until_complete(
                catub(
                    functions.channels.InviteToChannelRequest(
                        channel=BOTLOG_CHATID,
                        users=[bot_details.username],
                    )
                )
            )
            catub.loop.run_until_complete(
                catub(
                    functions.channels.InviteToChannelRequest(
                        channel=Config.PM_LOGGER_GROUP_ID,
                        users=[bot_details.username],
                    )
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def startupmessage():
    try:
        if BOTLOG:
            Config.CATUBLOGO = await catub.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/4e3ba8e8f7e535d5a2abe.jpg",
                caption="**Your CatUserbot has been started successfully.**",
                buttons=[(Button.url("Support", "https://t.me/catuserbot"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await catub.check_testcases()
            message = await catub.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**Ok Bot is Back and Alive.**"
            await catub.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await catub.send_message(
                    msg_details[0],
                    f"{cmdhr}ping",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


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

verifyLoggerGroup()
add_bot_to_logger_group()

path = "userbot/plugins/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(shortname.replace(".py", ""))
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break
            else:
                os.remove(Path(f"userbot/plugins/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"userbot/plugins/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")

path = "userbot/assistant/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(
                            shortname.replace(".py", ""),
                            plugin_path="userbot/assistant",
                        )
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break

            else:
                os.remove(Path(f"userbot/assistant/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"userbot/assistant/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")
            LOGS.info(f"{e.args}")

print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
print("Yay your userbot is officially working.!!!")
print(
    f"Congratulation, now type {cmdhr}alive to see message if catub is live\
      \nIf you need assistance, head to https://t.me/catuserbot_support"
)
print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")

verifyLoggerGroup()
add_bot_to_logger_group()
catub.loop.create_task(startupmessage())

if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    catub.run_until_disconnected()
