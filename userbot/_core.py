from userbot import bot
from telethon import events
from userbot.utils import command, load_module
from config import Config
import importlib
from pathlib import Path
from userbot import BAN_PLUG
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
                path = Path(downloaded_file_name)
                shortname = path.stem
                name = "userbot.plugins.{}".format(shortname.replace(".py", ""))
                spec = importlib.util.spec_from_file_location(name, path)
                mod = importlib.util.module_from_spec(spec)
                mod.bot = bot
                mod.Config = Config
                mod.command = command
                # support for uniborg
                sys.modules["uniborg.util"] = userbot.utils
                mod.borg = bot
                # support for paperplaneextended
                sys.modules["userbot.events"] = userbot.utils
                spec.loader.exec_module(mod)  # pylint:disable=E0602
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! Cannot install this plugin.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.send (?P<shortname>\w+)$", outgoing=True)
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./userbot/plugins/{}.py".format(input_str)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit("Uploaded {} in {} seconds".format(input_str, time_taken_in_ms))
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
