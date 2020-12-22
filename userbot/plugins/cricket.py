"""
Created by @Jisan7509
plugin for Cat_Userbot
"""

from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(pattern=r"score$"))
@bot.on(sudo_cmd(pattern=r"score$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    chat = "@cricbuzz_bot"
    reply_to_id = event.message
    catevent = await edit_or_reply(event, "```Gathering info...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message("/score")
            respond = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("Unblock @cricbuzz_bot & try again")
            return
        if respond.text.startswith("I can't find that"):
            await catevent.edit("sorry i can't find it")
        else:
            await catevent.delete()
            await event.client.send_message(
                event.chat_id, respond.message, reply_to=reply_to_id
            )
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, msg.id, response.id, respond.id]
        )


@bot.on(admin_cmd(pattern=r"cric (.*)"))
@bot.on(sudo_cmd(pattern=r"cric (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    details = event.pattern_match.group(1)
    chat = "@cricbuzz_bot"
    reply_to_id = event.message
    catevent = await edit_or_reply(event, "```Gathering info...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(f"{details}")
            respond = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("Unblock @cricbuzz_bot & try again")
            return
        if respond.text.startswith("I can't find that"):
            await catevent.edit("sorry i can't find it")
        else:
            await catevent.delete()
            await event.client.send_message(
                event.chat_id, respond.message, reply_to=reply_to_id
            )
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, msg.id, response.id, respond.id]
        )


CMD_HELP.update(
    {
        "cricket": "**Plugin :** `cricket`\
      \n\n**  • Syntax : **`.score` \
      \n**  • Function : **__To see score of ongoing matches.__\
      \n\n**  • Syntax : **`.cric <commnd>`\
      \n**  • Function : **__That will send details like scoreboard or commentary.__\
      \n\n**  • Example :-** `.cric /scorecard_30....`"
    }
)
