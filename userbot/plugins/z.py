from telethon import events
from userbot.utils import admin_cmd

@borg.on(admin_cmd("zen"))
async def handler(event):
    await event.reply("hey")
