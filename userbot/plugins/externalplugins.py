import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from userbot.utils import load_module
from var import Var

from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd


@borg.on(admin_cmd(pattern="extdl$", outgoing=True))
@borg.on(sudo_cmd(pattern="extdl$", allow_sudo=True))
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
    \n**Usage : **To install external plugins Create a private channel and post there all your external modules and set a var in heroku as `PLUGIN_CHANNEL` and value with channel id \
    so after each restart or update simply type  `.extdl` to install all external modules\
    "
    }
)
