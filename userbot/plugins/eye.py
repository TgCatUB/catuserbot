"""COMMAND : .eye"""
from telethon import events
import asyncio
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="eye$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 10)
    #input_str = event.pattern_match.group(1)
    #if input_str == "eye":
    await event.edit("👁👁")
    animation_chars = [

            "👁👁\n  👄  =====> Hey, How are you?",
            "👁👁\n  👅  =====> Everything okay?",    
            "👁👁\n  💋  =====> Why are you staring at this?",
            "👁👁\n  👄  =====> You idiot",
            "👁👁\n  👅  =====> Go away",    
            "👁👁\n  💋  =====> Stop laughing",
            "👁👁\n  👄  =====> It's not funny",
            "👁👁\n  👅  =====> I guess ur still looking",    
            "👁👁\n  💋  =====> Ok man 😑",
            "👁👁\n  👄  =====> I go away then"
        ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])
    await asyncio.sleep(animation_interval)    
    await event.delete()    
