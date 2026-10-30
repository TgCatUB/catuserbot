import glob
import os
import sys
import httpx
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import catub
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import del_keyword_collectionlist, get_item_collectionlist
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

LOGS = logging.getLogger("CatUBStartUP")
cmdhr = Config.COMMAND_HAND_LER

VPS_NOLOAD = ["heroku"]


async def setup_bot():
    """
    To set up bot for userbot
    """
    try:
        await catub.connect()
        config = await catub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == catub.session.server_address:
                if catub.session.dc_id != option.id:
                    LOGS.warning(f"Fixed DC ID in session from {catub.session.dc_id} to {option.id}")
                catub.session.set_dc(option.id, option.ip_address, option.port)
                catub.session.save()
                break
        bot_details = await catub.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await catub.start(bot_token=Config.TG_BOT_USERNAME)
        catub.me = await catub.get_me()
        if catub.me is None:
            LOGS.error(
                "catub.me is None. Make sure your STRING_SESSION is valid and the bot can log in.",
            )
            sys.exit()
        catub.uid = catub.tgbot.uid = utils.get_peer_id(catub.me)
        if Config.OWNER_ID == 0:
            if catub.me is not None:
                Config.OWNER_ID = utils.get_peer_id(catub.me)
            else:
                LOGS.error("catub.me is None, cannot set OWNER_ID.")
                sys.exit()
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {e}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.CATUBLOGO = await catub.tgbot.send_file(
                BOTLOG_CHATID,
                "https://graph.org/file/4e3ba8e8f7e535d5a2abe.jpg",
                caption="**Your CatUserbot has been started successfully.**",
                buttons=[(Button.url("Support", "https://t.me/thecatub"),)],
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


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await catub.tgbot.get_me()
    try:
        await catub(functions.messages.AddChatUserRequest(chat_id=chat_id, user_id=bot_details.username, fwd_limit=1000000))
    except BaseException:
        try:
            await catub(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder, extfolder=None):
    """
    To load plugins from the mentioned folder
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"userbot/{folder}/*.py"
        plugin_path = f"userbot/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []

    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")

            conditionForLoadingPlugins = pluginname in Config.LOAD_ONLY if len(Config.LOAD_ONLY) else ((pluginname not in Config.NO_LOAD) and (pluginname not in VPS_NOLOAD))

            try:
                if not conditionForLoadingPlugins:
                    LOGS.info(f"skipping {pluginname}")
                    continue

                flag = True
                check = 0
                while flag:
                    try:
                        load_module(pluginname, plugin_path=plugin_path)
                        if shortname in failure:
                            failure.remove(shortname)
                        success += 1
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if shortname not in failure:
                            failure.append(shortname)
                        if check > 5:
                            break
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                LOGS.info(f"unable to load {shortname} because of error {e}\nBase Folder {plugin_path}")
    if extfolder:
        if not failure:
            failure.append("None")
        return success, failure


async def check_send_message_permission(groupID, varName):
    try:
        entity = await catub.get_entity(groupID)
        if not isinstance(entity, types.User) and not entity.creator:
            if (entity.default_banned_rights and entity.default_banned_rights.send_messages) or not entity.admin_rights.post_messages:
                LOGS.info(f"Permissions missing to send messages for the specified {varName}.")
            if (entity.default_banned_rights and entity.default_banned_rights.invite_users) or not entity.admin_rights.invite_users:
                LOGS.info(f"Permissions missing to addusers for the specified {varName}.")
    except ValueError:
        LOGS.error(f"{varName} cannot be found. Make sure it's correct.")
    except TypeError:
        LOGS.error(f"{varName} is unsupported. Make sure it's correct.")
    except Exception as e:
        LOGS.error(f"An Exception occured upon trying to verify the {varName}.\n{str(e)}")


async def verifyLoggerGroup():
    """Will verify the both loggers group"""
    flag = False
    if BOTLOG:
        await check_send_message_permission(BOTLOG_CHATID, "PRIVATE_GROUP_BOT_API_ID")
    else:
        descript = "Don't delete this group or change to group(If you change group all your previous snips, welcome will be lost.)"
        _, groupid = await create_supergroup("CatUserbot BotLog Group", catub, Config.TG_BOT_USERNAME, descript)
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        LOGS.info("Private Group for PRIVATE_GROUP_BOT_API_ID is created successfully and added to vars.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        await check_send_message_permission(PM_LOGGER_GROUP_ID, "PM_LOGGER_GROUP_ID")
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)


async def install_externalrepo(repo, branch, cfolder):
    CATREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if CATBRANCH := branch:
        repourl = os.path.join(CATREPO, f"tree/{CATBRANCH}")
        gcmd = f"git clone -b {CATBRANCH} {CATREPO} {cfolder}"
        errtext = f"There is no branch with name `{CATBRANCH}` in your external repo {CATREPO}. Recheck branch name and correct it in vars(`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = CATREPO
        gcmd = f"git clone {CATREPO} {cfolder}"
        errtext = f"The link({CATREPO}) you provided for `EXTERNAL_REPO` in vars is invalid. please recheck that link"
    api_url = repourl.replace("github.com", "api.github.com/repos").replace("tree", "branches")
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        response = await client.get(api_url)
    if response.status_code != 200:
        LOGS.error(errtext)
        return await catub.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error("There was a problem in cloning the external repo. please recheck external repo link")
        return await catub.tgbot.send_message(
            BOTLOG_CHATID,
            "There was a problem in cloning the external repo. please recheck external repo link",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    success, failure = await load_plugins(folder="userbot", extfolder=cfolder)
    return repourl, cfolder, success, failure
