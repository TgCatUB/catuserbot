# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events, utils
from telethon.tl import types
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="resend"))
async def _(event):
    await event.delete()
    m = await event.get_reply_message()
    if not m:
        return
    await event.respond(m)
