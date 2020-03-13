# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio

from telethon import events
import telethon.utils

from uniborg import util


async def get_target_message(event):
    if event.is_reply and (await event.get_reply_message()).from_id == borg.uid:
        return await event.get_reply_message()
    async for message in borg.iter_messages(
            await event.get_input_chat(), limit=20):
        if message.out:
            return message


async def await_read(chat, message):
    chat = telethon.utils.get_peer_id(chat)

    async def read_filter(read_event):
        return (read_event.chat_id == chat
                and read_event.is_read(message))
    fut = borg.await_event(events.MessageRead(inbox=False), read_filter)

    if await util.is_read(borg, chat, message):
        fut.cancel()
        return

    await fut


@borg.on(util.admin_cmd(pattern="(del)(?:ete)?$"))
@borg.on(util.admin_cmd(pattern="(edit)(?:\s+(.*))?$"))
async def delete(event):
    await event.delete()
    command = event.pattern_match.group(1)
    if command == 'edit':
        text = event.pattern_match.group(2)
        if not text:
            return
    target = await get_target_message(event)
    if target:
        chat = await event.get_input_chat()
        await await_read(chat, target)
        await asyncio.sleep(.5)
        if command == 'edit':
            await borg.edit_message(chat, target, text)
        else:
            await borg.delete_messages(chat, target, revoke=True)
