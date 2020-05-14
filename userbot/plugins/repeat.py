import asyncio
from asyncio import wait
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="repeat ?(.*)"))
async def _(event):
    message = event.text[10:]
    count = int(event.text[8:10])
    repmessage = message * count
    await wait([event.respond(repmessage)])
    await event.delete()
