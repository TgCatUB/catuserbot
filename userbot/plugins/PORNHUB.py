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

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    input_str = event.pattern_match.group(1)

    if input_str == "pornhub":

        await event.edit(input_str)

        animation_chars = [

            "P_",

            "PO_",

            "POR_",

            "PORN_",
            
            "PORNH_",
            
            "PORNHU_",
            
           "PORNHUB_", 
           
           "PORNHUB",

        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 10])


@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    input_str = event.pattern_match.group(1)

    if input_str == "amore":

        await event.edit(input_str)

        animation_chars = [

            "A_",

            "AM_",

            "AMO_",

            "AMOR_",
            
            "AMORE_",
            
            "AMORE❤_",
            
            ".-.",

        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 10])



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

    animation_interval = 0.5

    animation_ttl = range(0, 101)

    input_str = event.pattern_match.group(1)

    if input_str == "sexy":

        await event.edit(input_str)

        animation_chars = [

            "S_",

            "SE_",

            "SEX_",

            "SEXY_",
            
            "SEXY👄_",
            
            "SEXY👄",
            
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 10])
