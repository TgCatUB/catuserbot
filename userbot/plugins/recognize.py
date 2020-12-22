# credits: @Mr_Hops

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(pattern="recognize ?(.*)"))
@bot.on(sudo_cmd(pattern="recognize ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user's media message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to media file")
        return
    chat = "@Rekognition_Bot"
    if reply_message.sender.bot:
        await event.edit("Reply to actual users message.")
        return
    cat = await edit_or_reply(event, "recognizeing this media")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await cat.edit("unblock @Rekognition_Bot and try again")
            return
        if response.text.startswith("See next message."):
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            response = await response
            msg = response.message.message
            await cat.edit(msg)
        else:
            await cat.edit("sorry, I couldnt find it")

        await event.client.send_read_acknowledge(conv.chat_id)


CMD_HELP.update(
    {
        "recognize": "**Plugin : **`recognize`\
        \n\n**Syntax : **`.recognize reply this to any image file`\
    \n**Function : **__Get information about an image using AWS Rekognition.\
    \nFind out information including detected labels, faces. text and moderation tags.__"
    }
)
