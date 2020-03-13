"""Use cmd `.cry` to cry"""

from telethon import events
from uniborg.util import admin_cmd
import asyncio





@borg.on(admin_cmd(pattern="lcry"))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 1
    

    animation_ttl = range(0, 103)

    

  

    await event.edit("crying")

    animation_chars = [

            ";__",
            ";___",
            ";____",
            ";_____",
            ";______",
            ";_______",
            ";________",
            ";__________",
            ";____________",
            ";______________",
            ";________________",
            ";__________________",
            ";____________________",
            ";______________________",
            ";________________________",
            ";_________________________",
            ";_________________________",
            ";________________________",
            ";_______________________",
            ";______________________",
            ";_____________________",
            ";____________________",
            ";___________________",
            ";__________________",
            ";_________________",
            ";________________",
            ";_______________",
            ";_____________",
            ";___________",
            ";_________",
            ";_______",
            ";_____",
            ";____",
            ";___",
            ";__",
            ";You made me `CRY`"
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])
