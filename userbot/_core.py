from userbot import bot
from telethon import events
from userbot.utils import command, remove_plugin, load_module
from var import Var
import importlib
from pathlib import Path
from userbot import LOAD_PLUG
import sys
import asyncio
import traceback
import os
import userbot.utils
from datetime import datetime

DELETE_TIMEOUT = 5

@command(pattern="^.install", outgoing=True)
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "userbot/plugins/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! This plugin is already installed/pre-installed.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.unload (?P<shortname>\w+)$", outgoing=True)
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"Unloaded {shortname} successfully")
    except Exception as e:
        await event.edit("Successfully unload {shortname}\n{}".format(shortname, str(e)))

@command(pattern="^.load (?P<shortname>\w+)$", outgoing=True)
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except:
            pass
        load_module(shortname)
        await event.edit(f"Successfully loaded {shortname}")
    except Exception as e:
        await event.edit(f"Could not load {shortname} because of the following error.\n{str(e)}")
