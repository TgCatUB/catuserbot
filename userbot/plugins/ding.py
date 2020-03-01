"""Emoji

Available Commands:

.ding"""

from telethon import events
import asyncio
from userbot.utils import admin_cmd



#@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
@borg.on(admin_cmd(pattern="ding ?(.*)"))
async def _(event):
    animation_interval = 0.3

    animation_ttl = range(0, 30)
    
    animation_chars = [
        
            "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
            "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
            "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
            "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
            "⬜⬜⬛⬛🔴\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",    
            "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
            "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
            "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
            "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
            
 ]
    
    if event.fwd_from:

        return

    await event.edit("ding..dong..ding..dong ...")

    await asyncio.sleep(4)
    
    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])
