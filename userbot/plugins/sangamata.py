import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP, parse_pre, sanga_seperator


@bot.on(admin_cmd(pattern="(sg|sgu)($| (.*))"))
@bot.on(sudo_cmd(pattern="(sg|sgu)($| (.*))", allow_sudo=True))
async def _(event):
    # https://t.me/catuserbot_support/181159
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        catevent = await edit_or_reply(
            event,
            "`reply to  user's text message to get name/username history or give userid`",
        )
        await asyncio.sleep(5)
        return await catevent.delete()
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                catevent = await edit_or_reply(
                    event, "`Give userid or username to find name history`"
                )
                await asyncio.sleep(5)
                return await catevent.delete()
            uid = u.id
    else:
        uid = reply_message.from_id
    chat = "@SangMataInfo_bot"
    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await catevent.edit("`unblock @Sangmatainfo_bot and then try`")
            await asyncio.sleep(5)
            return await catevent.delete()
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await catevent.edit("`bot can't fetch results`")
        await asyncio.sleep(5)
        return await catevent.delete()
    if "No records found" in responses:
        await catevent.edit("`The user doesn't have any record`")
        await asyncio.sleep(5)
        return await catevent.delete()
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    if cmd == "sg":
        sandy = None
        for i in names:
            if sandy:
                await event.reply(i, parse_mode=parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=parse_pre)
    elif cmd == "sgu":
        sandy = None
        for i in usernames:
            if sandy:
                await event.reply(i, parse_mode=parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "sangamata": "**Plugin : **`sangamata`\
    \n\n**Syntax : **`.sg <username/userid/reply>`\
    \n**Function : **__Shows you the previous name history of user.__\
    \n\n**Syntax : **`.sgu <username/userid/reply>`\
    \n**Function : **__Shows you the previous username history of user.__\
    "
    }
)
