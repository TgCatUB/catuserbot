from telethon import events
import asyncio
from userbot.utils import admin_cmd
import os

@borg.on(admin_cmd(pattern="ttf ?(.*)"))
async def get(event):
    name = event.text[5:]
    if name is None:
        await event.edit("reply to text message as `.ttf <file name>`")
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await borg.send_file(event.chat_id,name,force_document=True)
        os.remove(name)
    else:
        await event.edit("reply to text message as `.ttf <file name>`")
