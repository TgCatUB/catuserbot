#By STARKTM1
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.plane", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("✈-------------")
    await event.edit("-✈------------")
    await event.edit("--✈-----------")
    await event.edit("---✈----------")
    await event.edit("----✈---------")
    await event.edit("-----✈--------")
    await event.edit("------✈-------")
    await event.edit("-------✈------")
    await event.edit("--------✈-----") 
    await event.edit("---------✈----")
    await event.edit("----------✈---")
    await event.edit("-----------✈--")
    await event.edit("------------✈-")
    await event.edit("-------------✈")
    await asyncio.sleep(3)
    await event.delete()

