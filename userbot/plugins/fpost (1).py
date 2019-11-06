# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
""" Command: .fpost word

credit: @r4v4n4"""

import string

from telethon import events
from telethon.tl import types

msg_cache = {}


@borg.on(events.NewMessage(pattern=r"\.fpost\s+(.*)", outgoing=True))
async def _(event):
    await event.delete()
    text = event.pattern_match.group(1)
    destination = await event.get_input_chat()

    for c in text.lower():
        if c not in string.ascii_lowercase:
            continue
        if c not in msg_cache:
            async for msg in borg.iter_messages(None, search=c):
                if msg.raw_text.lower() == c and msg.media is None:
                    msg_cache[c] = msg
                    break
        await borg.forward_messages(destination, msg_cache[c])
