from telethon import events
import asyncio
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="ttf ?(.*)"))
async def get(event):
    name = event.text[5:]
    m = await event.get_reply_message()
    with open(name, "w") as f:
        f.write(m.message)
    await event.delete()
    await borg.send_file(event.chat_id,name,force_document=True)
