"""Emoji
Available Commands:
.fuk
.sex
.kiss
"""

from telethon import events
import asyncio
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="fuk$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 101)
    animation_chars = [

            "👉       ✊️",
            "👉     ✊️",
            "👉  ✊️",
            "👉✊️💦"
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])

@borg.on(admin_cmd(pattern="sex$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 101)
    animation_chars = [
            "🤵       👰",
            "🤵     👰",
            "🤵  👰",
            "🤵👼👰"
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])


@borg.on(admin_cmd(pattern="kiss$"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 101)
    animation_chars = [
            "🤵       👰",
            "🤵     👰",
            "🤵  👰",
            "🤵💋👰"
        ]
    for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])
