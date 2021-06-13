import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

import userbot
from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import catub
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import gvarstatus
from .pluginmanager import load_module

LOGS = logging.getLogger("CatUserbot")
cmdhr = Config.COMMAND_HAND_LER


async def verifyLoggerGroup():
    flag = False
    if BOTLOG:
        try:
            entity = await catub.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID cannot be found. Make sure it's correct."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID is unsupported. Make sure it's correct."
            )
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "Don't delete this group or change to group(If you change group all your previous snips, welcome will be lost.)"
        group_data = await create_supergroup("CatUserbot BotLog Group" ,catub, Config.TG_BOT_USERNAME,descript)
        addgvar("PRIVATE_GROUP_BOT_API_ID",group_data[1])
        print("Private Group for PRIVATE_GROUP_BOT_API_ID is created succesfully and added to vars.")
        flag = True
    if PM_LOGGER_GROUP_ID:
        try:
            entity = await catub.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID cannot be found. Make sure it's correct.")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID is unsupported. Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PM_LOGGER_GROUP_ID.\n"
                + str(e)
            )
    else:
        descript = "Don't delete this group or change to group."
        group_data = await create_supergroup("CatUserbot PM Logger Group" ,catub, Config.TG_BOT_USERNAME,descript)
        addgvar("PM_LOGGER_GROUP_ID",group_data[1])
        print("Private Group for PM_LOGGER_GROUP_ID is created succesfully and added to vars.")
        flag = True
    if flag:
        await catub.reload()

