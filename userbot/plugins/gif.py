from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import os 
from . import CMD_HELP , unzip
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

if not os.path.isdir("./temp"):
    os.makedirs("./temp")

@borg.on(admin_cmd(pattern="gif$"))
async def _(event):
    catreply = await event.get_reply_message()
    if not catreply or not catreply.media or not catreply.media.document:
        return await edit_or_reply(event , "`Stupid!, This is not animated sticker.`")
    elif catreply.media.document.mime_type != 'application/x-tgsticker':
        return await edit_or_reply(event , "`Stupid!, This is not animated sticker.`")
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@tgstogifbot"
    catevent = await edit_or_reply(event , "`Converting to gif ...`")
    async with event.client.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await event.client.send_file(chat, catreply.media)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return await catevent.edit("`This file is not supported`")
            catresponse = response if response.media else await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            catfile = await event.client.download_media(catresponse,"./temp")
            catgif = await unzip(catfile)
            await event.client.send_file(event.chat_id, catgif ,support_streaming=True,force_document=False, reply_to=reply_to_id)
            await catevent.delete()
        except YouBlockedUserError:
            await catevent.edit("Unblock @tgstogifbot")
            return

async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response
