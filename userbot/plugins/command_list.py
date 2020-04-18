from telethon import events
import subprocess
import asyncio
import time
<<<<<<< HEAD
from userbot.utils import admin_cmd
=======
>>>>>>> e5ef0b3993bbed07fa8182df63a2a5da234c5941


@command(pattern="^.cmds", outgoing=True)
async def install(event):
    if event.fwd_from:
        return
    cmd = "ls userbot/plugins"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
<<<<<<< HEAD
    OUTPUT = f"**List of Plugins:**\n{o}\n\n**TIP:** __If you want to know the commands for a plugin, do:-__ \n `.help <plugin name>` **without the < > brackets.**\n__All plugins might not work directly."
=======
    OUTPUT = f"**List of Plugins:**\n{o}\n\n**TIP:** __If you want to know the commands for a plugin, do:-__ \n `.help <plugin name>` **without the < > brackets.**\n__All plugins might not work directly. Visit__ @XtraTgChat __for assistance.__"
>>>>>>> e5ef0b3993bbed07fa8182df63a2a5da234c5941
    await event.edit(OUTPUT)
