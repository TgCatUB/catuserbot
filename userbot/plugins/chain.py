# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from telethon.tl.functions.messages import SaveDraftRequest

from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd


@borg.on(admin_cmd(pattern="chain$"))
@borg.on(sudo_cmd(pattern="chain$", allow_sudo=True))
async def _(event):
    await event.edit("Counting...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await borg(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f"Chain length: {count}")


CMD_HELP.update(
    {
        "chain": "**SYNTAX :** `.chain`\
    \n**USAGE : **Reply this command to any converstion where you want to find length of converstion(Only tagged chain will count ) \
    "
    }
)
