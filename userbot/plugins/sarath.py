"""Emoji

Available Commands:

.sarath"""

from telethon import events
import asyncio
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="sarath$"))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.3

    animation_ttl = range(0, 30)

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
