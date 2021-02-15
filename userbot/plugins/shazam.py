import requests
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(pattern="szm$", outgoing=True))
@bot.on(sudo_cmd(pattern="szm$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "```Reply to an audio message.```")
        return
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    catevent = await edit_or_reply(event, "```Identifying the song```")
    async with event.client.conversation(chat) as conv:
        try:
            start_msg = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(reply_message)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await catevent.edit("An error while identifying the song. Try to use a 5-10s long audio message.")
            await catevent.edit("Wait just a sec...")
            result = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Please unblock (@auddbot) and try again```")
            return
    namem = f"**Song Name : **`{result.text.splitlines()[0]}`\
        \n\n**Details : **__{result.text.splitlines()[2]}__"
    await catevent.edit(namem)

CMD_HELP.update(
    {
        "shazam": "**Plugin : **`shazam`\
    \n\n**  •  Syntax : **`.szm` reply to an audio file\
    \n**  •  Function :**Reverse search of song/music\
    "
    }
)
