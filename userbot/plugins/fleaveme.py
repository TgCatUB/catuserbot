#Credit: @r4v4n4
"""Emoji

Available Commands:

.fleave"""


from telethon import events
import asyncio
from userbot.utils import admin_cmd


#@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
@borg.on(admin_cmd(pattern="fleaveme ?(.*)"))
async def _(event):
    animation_interval = 1

    animation_ttl = range(0, 17)
    animation_chars = [
        
            "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
            "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",    
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
            "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
            "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
            "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
            "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️"
 ]
    if event.fwd_from:

        return

    await event.edit("fleaveme....")
    
    await asyncio.sleep(2)
    
    for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 17])
