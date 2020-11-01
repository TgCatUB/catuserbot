# created by @Mr_Hops
"""
video meme mashup:
Syntax: .mash <text>
"""
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP
from userbot.utils import admin_cmd, edit_or_reply, sudo_cmd


@bot.on(admin_cmd(pattern="mash ?(.*)"))
@bot.on(sudo_cmd(pattern="mash ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@vixtbot"
    catevent = await edit_or_reply(event, "```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(input_str)
            respond = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("Unblock @vixtbot")
            return
        if respond.text.startswith("I can't find that"):
            await catevent.edit("sorry i can't find it")
        else:
            await catevent.delete()
            await event.client.send_file(event.chat_id, respond, reply_to=reply_to_id)
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, msg.id, response.id, respond.id]
        )


CMD_HELP.update(
    {
        "mashup": "__**PLUGIN NAME :** Mashup__\
      \n\n📌** CMD ➥** `.mash` <text> \
      \n**USAGE   ➥  **Send you the related video message of given text . "
    }
)
