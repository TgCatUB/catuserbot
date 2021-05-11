import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from ..Config import Config
from ..utils import load_module
from . import BOTLOG, BOTLOG_CHATID, catub

plugin_category = "tools"

if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await catub.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if os.path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await catub.download_media(
                await catub.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            if BOTLOG:
                await catub.send_message(
                    BOTLOG_CHATID,
                    f"Installed Plugin `{os.path.basename(downloaded_file_name)}` successfully.",
                )

    catub.loop.create_task(install())
