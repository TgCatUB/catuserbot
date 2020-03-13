# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Snips
Available Commands:
.snips
.snipl
.snipd"""
from telethon import events, utils
from telethon.tl import types
from sql_helpers.snips_sql import get_snips, add_snip, remove_snip, get_all_snips
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern=r'\#(\S+)', outgoing=True))
async def on_snip(event):
    name = event.pattern_match.group(1)
    snip = get_snips(name)
    if snip:
        msg_o = await event.client.get_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            ids=int(snip.f_mesg_id)
        )
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        media_message = msg_o.media
        if isinstance(media_message, types.MessageMediaWebPage):
            media_message = None
        await event.client.send_message(
            event.chat_id,
            msg_o.message,
            reply_to=message_id,
            file=media_message
        )
        await event.delete()


@borg.on(admin_cmd(pattern="snips (.*)"))
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        msg_o = await event.client.forward_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            messages=msg,
            from_peer=event.chat_id,
            silent=True
        )
        add_snip(name, msg_o.id)
        await event.edit("snip {name} saved successfully. Get it with #{name}".format(name=name))
    else:
        await event.edit("Reply to a message with `snips keyword` to save the snip")


@borg.on(admin_cmd(pattern="snipl"))
async def on_snip_list(event):
    all_snips = get_all_snips()
    OUT_STR = "Available Snips:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 #{a_snip.snip} \n"
    else:
        OUT_STR = "No Snips. Start Saving using `.snips`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "snips.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Snips",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(OUT_STR)


@borg.on(admin_cmd(pattern="snipd (\S+)"))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_snip(name)
    await event.edit("snip #{} deleted successfully".format(name))
