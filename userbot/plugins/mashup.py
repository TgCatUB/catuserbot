# created by @Mr_Hops
"""
video meme mashup:
Syntax: .mash <text>
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot.utils import sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="mash ?(.*)"))
@bot.on(sudo_cmd(pattern="mash ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@vixtbot"
    catevent = await edit_or_reply(event, "```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=285336877)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await catevent.edit("Unblock @vixtbot")
            return
        if response.text.startswith("I can't find that"):
            await catevent.edit("sorry i can't find it")
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id, response.message, reply_to=reply_to_id
            )


CMD_HELP.update(
    {
        "mashup": "`.mash` <text> :\
      \n**USAGE:** Sends you the related video message of given text. "
    }
)
