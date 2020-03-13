"""Send Chat Actions
Syntax: .sca <option>
Options: typing, contact, game, location, voice, round, video, photo, document, cancel"""

import asyncio
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="sca ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(10)  # type for 10 seconds
