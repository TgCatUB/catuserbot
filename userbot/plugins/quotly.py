"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from .. import process
from ..utils import admin_cmd, sudo_cmd


@borg.on(admin_cmd(pattern="q(?: |$)(.*)"))
async def stickerchat(catquotes):
    if catquotes.fwd_from:
        return
    reply = await catquotes.get_reply_message()
    if not reply:
        await catquotes.edit("I cant quote the message . reply to a message")
        return
    fetchmsg = reply.message
    repliedreply = await reply.get_reply_message()
    if reply.media:
        if reply.media.document.mime_type in ("mp4"):
            await catquotes.edit("animated stickers and mp4 formats are not supported")
            return
    await catquotes.delete()
    user = (
        await borg.get_entity(reply.forward.sender) if reply.fwd_from else reply.sender
    )
    res, catmsg = await process(fetchmsg, user, borg, reply, repliedreply)
    if not res:
        return
    catmsg.save("./temp/sticker.webp")
    await borg.send_file(catquotes.chat_id, "./temp/sticker.webp", reply_to=reply)
    os.remove("./temp/sticker.webp")


@borg.on(admin_cmd(pattern="qbot(?: |$)(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```Reply to text message```")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    await event.edit("```Making a Quote```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
            return
        await borg.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("Hi!"):
            await event.edit(
                "```Can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


@borg.on(sudo_cmd(pattern="qbot(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.reply("```Reply to text message```")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.reply("```Reply to actual users message.```")
        return
    cat = await event.reply("```Making a Quote```")
    await borg.send_read_acknowledge(conv.chat_id)
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
            return
        if response.text.startswith("Hi!"):
            await event.reply(
                "```Can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await cat.delete()
            await event.client.send_message(event.chat_id, response.message)
