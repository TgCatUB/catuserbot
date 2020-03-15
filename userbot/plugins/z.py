from telethon import events
from uniborg.util import admin_cmd

@borg.on(admin_cmd("hi"))
async def handler(event):
    await event.reply("hey")
