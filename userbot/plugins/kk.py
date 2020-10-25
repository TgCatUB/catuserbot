"""command: .kk By @Grandpaa_please """


import random

from telethon import events


@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str == "kk":
        r = random.randint(0, 3)
        logger.debug(r)
        if r == 0:
            await event.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
        else:
            await event.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")
