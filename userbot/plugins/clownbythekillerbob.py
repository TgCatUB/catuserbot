
from telethon import events

import asyncio
from userbot.utils import admin_cmd





@borg.on(admin_cmd(pattern=f"clown$", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.50

    animation_ttl = range(0, 117)

    animation_chars = [
        

            "COMMAND CREATE BY @Sur_vivor",
            "🤡️",
            "🤡🤡",
            "🤡🤡🤡",
            "🤡🤡🤡🤡",
            "🤡🤡🤡🤡🤡",
            "🤡🤡🤡🤡🤡🤡",    
            "🤡🤡🤡🤡🤡",
            "🤡🤡🤡🤡",
            "🤡🤡🤡",
            "🤡🤡",
            "🤡",
            "You",
            "You Are",
            "You Are A",
            "You Are A Clown 🤡"
        ]

     for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 117])
