"""Emoji

Available Commands:

.emoji shrug

.emoji apple

.emoji :/

.emoji -_-"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 1
    

    animation_ttl = range(0, 103)

    input_str = event.pattern_match.group(1)

    if input_str == "oof":

        await event.edit(input_str)

        animation_chars = [

            "o",
            "oo",    
            "ooo",
            "ooooo",
            "oooooo",
            "ooooooo",
            "oooooooo",
            "ooooooooo",
            "oooooooooo",    
            "ooooooooooo",
            "oooooooooooo",
            "ooooooooooooo",
            "oooooooooooooof"
        ]

        for i in animation_ttl:


            await event.edit(animation_chars[i % 103])
