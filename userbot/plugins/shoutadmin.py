"""Emoji
Available Commands:
.admem"""

from telethon import events
import asyncio

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"sadmin", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 96)
    input_str = event.pattern_match.group(1)
    if input_str == "sadmin":
        await event.edit(input_str)
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
            await event.edit(animation_chars[i % 96])
