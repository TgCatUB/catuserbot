import asyncio
import os
from datetime import datetime
from pathlib import Path

from ..utils import load_module, remove_plugin
from . import CMD_LIST, SUDO_LIST, hmention

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@bot.on(admin_cmd(pattern="install$"))
@bot.on(sudo_cmd(pattern="install$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_or_reply(
                    event,
                    f"Installed Plugin `{os.path.basename(downloaded_file_name)}`",
                )
            else:
                os.remove(downloaded_file_name)
                await edit_or_reply(
                    event, "Errors! This plugin is already installed/pre-installed."
                )
        except Exception as e:
            await edit_or_reply(event, str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@bot.on(admin_cmd(pattern=r"load (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"load (.*)", allow_sudo=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_or_reply(event, f"Successfully loaded {shortname}")
    except Exception as e:
        await edit_or_reply(
            event,
            f"Could not load {shortname} because of the following error.\n{str(e)}",
        )


@bot.on(admin_cmd(pattern=r"send (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"send (.*)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/plugins/{input_str}.py"
    if os.path.exists(the_plugin_file):
        start = datetime.now()
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await caat.edit(
            f"<b><i>➥ Plugin Name :- {input_str} .</i></b>\n<b><i>➥ Uploaded in {ms} seconds.</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
            parse_mode="html",
        )
    else:
        await edit_or_reply(event, "404: File Not Found")


@bot.on(admin_cmd(pattern=r"unload (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"unload (.*)", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"Unloaded {shortname} successfully")
    except Exception as e:
        await edit_or_reply(event, f"Successfully unload {shortname}\n{str(e)}")


@bot.on(admin_cmd(pattern=r"uninstall (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"uninstall (.*)", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    path = Path(f"userbot/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"There is no plugin with path {path} to uninstall it"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} is Uninstalled successfully")
    except Exception as e:
        await edit_or_reply(event, f"Successfully uninstalled {shortname}\n{str(e)}")


CMD_HELP.update(
    {
        "corecmds": "__**PLUGIN NAME :** Corecmds__\
    \n\n📌** CMD ➥** `.install` <replay on a plugin>\
    \n**USAGE   ➥  **To install external plugin in bot. \
    \n\n📌** CMD ➥** `.uninstall` <plugin name>\
    \n**USAGE   ➥  **To stop functioning of that plugin and remove that plugin from bot\
    \n\n📌** CMD ➥** `.send` <plugin name>\
    \n**USAGE   ➥  **To send/share loaded plugin.\
    \n\n📌** CMD ➥** `.unload` <plugin name>\
    \n**USAGE   ➥  **To unload any loaded plugin from bot.\
    \n\n📌** CMD ➥** `.load` <plugin name>\
    \n**USAGE   ➥  **To load plugins which are installed but unloaded in bot.\
    "
    }
)
