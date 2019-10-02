from telethon import events
import asyncio
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="dump ?(.*)"))
async def _(message):
    try:
        obj = message.pattern_match.group(1)
        if len(obj) != 3:
            raise IndexError
        inp = ' '.join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    u, t, g, o, s, n = inp.split(), '🗑', '<(^_^ <)', '(> ^_^)>', '⠀ ', '\n'
    h = [(u[0], u[1], u[2]), (u[0], u[1], ''), (u[0], '', '')]
    for something in reversed([y for y in ([''.join(x) for x in (
    f + (s, g, s + s * f.count(''), t), f + (g, s * 2 + s * f.count(''), t),
    f[:i] + (o, f[i], s * 2 + s * f.count(''), t), f[:i] + (s + s * f.count(''), o, f[i], s, t),
    f[:i] + (s * 2 + s * f.count(''), o, f[i], t), f[:i] + (s * 3 + s * f.count(''), o, t),
    f[:i] + (s * 3 + s * f.count(''), g, t))] for i, f in enumerate(reversed(h)))]):
        for something_else in something:
            await asyncio.sleep(0.3)
            try:
                await message.edit(something_else)
            except errors.MessageIdInvalidError:
                return
