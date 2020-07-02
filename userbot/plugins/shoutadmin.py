"""Emoji
Available Commands:
.admem"""

from telethon import events
import asyncio

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"sadmin", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 13)
    await event.edit("sadmin")
    animation_chars = [



            "@aaaaaaaaaaaaadddddddddddddmmmmmmmmmmmmmiiiiiiiiiiiiinnnnnnnnnnnnn",

            "@aaaaaaaaaaaaddddddddddddmmmmmmmmmmmmiiiiiiiiiiiinnnnnnnnnnnn",    

            "@aaaaaaaaaaadddddddddddmmmmmmmmmmmiiiiiiiiiiinnnnnnnnnnn",

            "@aaaaaaaaaaddddddddddmmmmmmmmmmiiiiiiiiiinnnnnnnnnn",

            "@aaaaaaaaadddddddddmmmmmmmmmiiiiiiiiinnnnnnnnn",

            "@aaaaaaaaddddddddmmmmmmmmiiiiiiiinnnnnnnn",

            "@aaaaaaadddddddmmmmmmmiiiiiiinnnnnnn",

            "@aaaaaaddddddmmmmmmiiiiiinnnnnn",

            "@aaaaadddddmmmmmiiiiinnnnn",    

            "@aaaaddddmmmmiiiinnnn",

            "@aaadddmmmiiinnn",

            "@aaddmmiinn",

            "@admin"

        ]

    for i in animation_ttl:
            await asyncio.sleep(1)
            await event.edit(animation_chars[i % 13])
