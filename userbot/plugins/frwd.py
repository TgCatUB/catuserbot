import asyncio
from userbot.utils import admin_cmd
from telethon import events

@bot.on(admin_cmd(incoming=True))
async def _(event):
    from_chnl = -1001562866430
    target_chnl = -1001489788469
    if not event.is_private:
        if event.chat_id == from_chnl:
            await event.client.send_message(target_chnl,event.message)
