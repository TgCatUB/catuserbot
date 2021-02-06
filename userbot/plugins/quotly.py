"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import convert_tosticker, process


@bot.on(admin_cmd(pattern="q(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="q(?: |$)(.*)", allow_sudo=True))
async def stickerchat(catquotes):
    if catquotes.fwd_from:
        return
    reply = await catquotes.get_reply_message()
    if not reply:
        await edit_or_reply(
            catquotes, "`I cant quote the message . reply to a message`"
        )
        return
    fetchmsg = reply.message
    repliedreply = None
    if reply.media and reply.media.document.mime_type in ("mp4"):
        await edit_or_reply(catquotes, "`this format is not supported now`")
        return
    catevent = await edit_or_reply(catquotes, "`Making quote...`")
    user = (
        await event.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, catmsg = await process(fetchmsg, user, catquotes.client, reply, repliedreply)
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    catmsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await catquotes.client.send_file(catquotes.chat_id, endfi, reply_to=reply)
    await catevent.delete()
    os.remove(endfi)


@bot.on(admin_cmd(pattern="rq(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="rq(?: |$)(.*)", allow_sudo=True))
async def stickerchat(catquotes):
    if catquotes.fwd_from:
        return
    reply = await catquotes.get_reply_message()
    if not reply:
        await edit_or_reply(
            catquotes, "`I cant quote the message . reply to a message`"
        )
        return
    fetchmsg = reply.message
    repliedreply = await reply.get_reply_message()
    if reply.media and reply.media.document.mime_type in ("mp4"):
        await edit_or_reply(catquotes, "`this format is not supported now`")
        return
    catevent = await edit_or_reply(catquotes, "`Making quote...`")
    user = (
        await event.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, catmsg = await process(fetchmsg, user, catquotes.client, reply, repliedreply)
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    catmsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await catquotes.client.send_file(catquotes.chat_id, endfi, reply_to=reply)
    await catevent.delete()
    os.remove(endfi)


@bot.on(admin_cmd(pattern="qbot(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="qbot(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    message = ""
    if reply:
        messages_id = []
        if input_str is not None and input_str.isnumeric():
            async for message in event.client.iter_messages(
                event.chat_id, limit=input_str, offset_id=reply.id, reverse=True
            ):
                if message.id != event.id:
                    messages_id.append(message.id)
        elif input_str is not None:
            message = input_str
        else:
            messages_id.append(reply.id)
    elif input_str is not None:
        message = input_str
    else:
        return await edit_delete(
            event, "`Either reply to message or give input to function properly`"
        )
    chat = "@QuotLyBot"
    catevent = await edit_or_reply(event, "```Making a Quote```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            if messages_id != []:
                await event.client.forward_messages(chat, messsages_id)
            elif message != "":
                await event.client.send_message(conv.chat_id, message)
            else:
                return await edit_delete(
                    catevent, "`I guess you have used a invalid syntax`"
                )
            response = await response
        except YouBlockedUserError:
            await catevent.edit("```Please unblock me (@QuotLyBot) u Nigga```")
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.delete()
        await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update(
    {
        "quotly": "**Plugin :** `quotly`\
        \n\n**•  Syntax : **`.q reply to messge`\
        \n**•  Function : **__Makes your message as sticker quote__\
        \n\n**•  Syntax : **`.q reply to messge`\
        \n**•  Function : **__Makes your message along with the previous replied message as sticker quote__\
        \n\n**•  Syntax : **`.qbot reply to messge`\
        \n**•  Function : **__Makes your message as sticker quote by @quotlybot__\
        "
    }
)
