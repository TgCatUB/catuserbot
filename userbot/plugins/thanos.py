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
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "thanoss":
        await event.edit(input_str)
        animation_chars = [
            "JINGLE BELLS",
            "THANOS SMELL LOKI NECKED SNAPPED AWAY",
            "PETER DIED TONY CRIED NOBODY SAVED THE DAY HEY!!",
            "Jingle bells Thanos smells Loki's necked snapped away Peter died Tony cried And nobody saved the day"
        ]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])
