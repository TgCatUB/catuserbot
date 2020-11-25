if Config.PLUGIN_CHANNEL:
    import os
    from pathlib import Path

    from telethon.tl.types import InputMessagesFilterDocument

    from ..utils import load_module
    from . import BOTLOG_CHATID

    async def install():
        documentss = await bot.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            downloaded_file_name = await bot.download_media(
                await bot.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await bot.send_message(
                    BOTLOG_CHATID,
                    f"Installed Plugin `{os.path.basename(downloaded_file_name)}` successfully.",
                ),
            else:
                await bot.send_message(
                    BOTLOG_CHATID,
                    f"Plugin `{os.path.basename(downloaded_file_name)}` has been pre-installed and cannot be installed.",
                )
                os.remove(downloaded_file_name)

    bot.loop.create_task(install())
