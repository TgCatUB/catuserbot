"""Emoji
Available Commands:
.emoji shrug
.emoji apple
.emoji :/
.emoji -_-"""

from telethon import events

import asyncio
from userbot.utils import admin_cmd 

@borg.on(admin_cmd(pattern="loveu"))
@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 117)

    input_str = event.pattern_match.group(1)

    if input_str == "loveu":

        await event.edit(input_str)

        animation_chars = [

            "😀",
            "👩‍🎨",
            "😁",    
            "😂",
            "🤣",
            "😃",
            "😄",
            "😅",
            "😊",
            "☺",
            "🙂",    
            "🤔",
            "🤨",
            "😐",
            "😑",
            "😶",
            "😣",
            "😥",
            "😮",    
            "🤐",
            "😯",
            "😴",
            "😔",
            "😕",
            "☹",
            "🙁",
            "😖",    
            "😞",
            "😟",
            "😢",
            "😭",
            "🤯",
            "💔",
            "❤",
            "i Love You❤",
           
            
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 117])
