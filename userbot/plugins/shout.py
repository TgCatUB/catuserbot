"""Shouts a message in MEME way
usage: .shout message
originaly from : @corsicanu_bot
"""

import asyncio

from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern=f"shout", outgoing=True))
async def shout(args):
    if args.fwd_from:
        return
    msg = "```"
    messagestr = args.text
    messagestr = messagestr[7:]
    text = " ".join(messagestr)
    result = []
    result.append(" ".join([s for s in text]))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "\n" + result
    await args.edit("`" + msg + "`")


@borg.on(admin_cmd(pattern=f"sadmin", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
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
        "@admin",
    ]
    for i in animation_ttl:
        await asyncio.sleep(1)
        await event.edit(animation_chars[i % 13])
