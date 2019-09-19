from userbot import bot
from telethon import events
from userbot.utils import command
from importlib import import_module
import sys
import asyncio
import traceback
import os
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
                imported_module = import_module(downloaded_file_name.replace("/", ".").replace(".py", ""))  # pylint:disable=E0602
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! Cannot install this plugin.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.load (?P<shortname>\w+)$", outgoing=True)
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        imported_module = import_module("userbot.plugins." + shortname)
        msg = await event.respond(f"Successfully (re)loaded plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load plugin {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")

@command(pattern="^.unload (?P<shortname>\w+)$", outgoing=True)
async def unload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        sys.path.append('userbot/plugins/')
        if shortname in sys.modules:  
            os.system(f"pkill -f userbot/plugin/{shortname}")
            msg = await event.respond(f"Successfully unloaded plugin {shortname}")
            await asyncio.sleep(DELETE_TIMEOUT)
            await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to unload plugin {shortname}: {trace_back}")
        await event.respond(f"Failed to unload plugin {shortname}: {e}")

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
