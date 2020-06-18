"""Emoji

Available Commands:

.sarath"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 30)

    input_str = event.pattern_match.group(1)

    if input_str == "sarath":

        await event.edit(input_str)

        animation_chars = [

            "S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",
            
            "◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",

            "◼️◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",

            "◼️◼️◼️️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",

            "◼️◼️◼️◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",

            "‎◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",
            
            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",
            
            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽",
   
            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\nS͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️S͓̽A͓̽R͓̽A͓̽T͓̽H͓̽◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",

            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
          
            "◼️◼️◼️◼️\n◼️◼️◼️◼️\n◼️◼️◼️◼️\n◼️◼️◼️◼️",
           
            "◼️◼️◼️\n◼️◼️◼️\n◼️◼️◼️",

            "◼️◼️\n◼️◼️",

            "◼️"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 30])
