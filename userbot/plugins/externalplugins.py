import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from userbot.utils import load_module
from var import Var

from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd


@bot.on(admin_cmd(pattern="extdl$", outgoing=True))
@bot.on(sudo_cmd(pattern="extdl$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    chat = Var.PLUGIN_CHANNEL
    documentss = await borg.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(total)
    await event.delete()
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(
            await borg.get_messages(chat, ids=mxo), "userbot/plugins/"
        )
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            await borg.send_message(
                event.chat_id,
                "Installed Plugin `{}` successfully.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )
        else:
            await borg.send_message(
                event.chat_id,
                "Plugin `{}` has been pre-installed and cannot be installed.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )


CMD_HELP.update(
    {
        "externalplugins": "**externalplugins**\
    \n**Syntax :** `.extdl`\
    \n**Usage : **Create a private channel and post all your external modules there and set a var in heroku as `PLUGIN_CHANNEL` and value with channel id \
    type  `.extdl` to install all external modules after each restart or update. \
    "
    }
)
