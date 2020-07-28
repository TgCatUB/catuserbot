"""COMMAND : .fk"""

from telethon import events

import asyncio

from userbot.utils import admin_cmd



@borg.on(admin_cmd(pattern="fk (.*)"))

async def _(event):

    if event.fwd_from:

        return
    
    name = event.pattern_match.group(1)
  
    animation_interval = 3

    animation_ttl = range(0, 103)

     

    #if input_str == "fk":

    await event.edit("👁👁")

    animation_chars = [

             f"👁👁\n  👄  =====> Abey {name} Chutiya",
             f"👁👁\n  👅  =====> Abey {name} Gay",    
             f"👁👁\n  💋  =====> Abey {name} Lodu",
             f"👁👁\n  👄  =====> Abey {name} Gandu",
             f"👁👁\n  💋  =====> Abey {name} Randi",
             f"👁👁\n  👄  =====> Abey {name} Betichod",
             f"👁👁\n  👅  =====> Abey {name} Behenchod",    
             f"👁👁\n  💋  =====> Abey {name} NaMard",
             f"👁👁\n  👄  =====> Abey {name} Lavde",
             f"👁👁\n  👅  =====> Abey {name} Bhosdk",    
             f"👁👁\n  👄  =====> Hi {name} Mc, How Are You Bsdk..."
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 103])