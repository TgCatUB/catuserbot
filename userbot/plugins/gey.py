"""COMMAND : .gey"""

from telethon import events

import asyncio

from userbot.utils import admin_cmd



@borg.on(admin_cmd(pattern="gey"))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 3

    animation_ttl = range(0, 103)

    #input_str = event.pattern_match.group(1)

    #if input_str == "gey":

    await event.edit("👁👁")

    animation_chars = [

            "👁👁\n  👄  =====> Abey NOBITA Gay",
            "👁👁\n  👅  =====> Abey VISHAL Gay",    
            "👁👁\n  💋  =====> Abey GOKU Gay",
            "👁👁\n  👄  =====> Abey RAHUL Gay",
            "👁👁\n  👅  =====> Abey SAM GAY",    
            "👁👁\n  💋  =====> Abey SANDEEP GAY",
            "👁👁\n  👄  =====> Abey DHANISH GAY",
            "👁👁\n  👅  =====> Abey EDWARD GAY",
            "👁👁\n  👅  =====> Abey RC GAY",    
            "👁👁\n  💋  =====> Abey Ja Na Chutiye",
            "👁👁\n  👄  =====> Hi All, How Are You Gays..."
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 103])
