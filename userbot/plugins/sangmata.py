import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from . import _format, sanga_seperator

plugin_category = "utils"


@catub.cat_cmd(
    pattern="sg(u)?(?: |$)(.*)",
    command=("sg", plugin_category),
    info={
        "header": "To get name history of the user.",
        "flags": {
            "u": "That is sgu to get username history.",
        },
        "usage": [
            "{tr}sg <username/userid/reply>",
            "{tr}sgu <username/userid/reply>",
        ],
        "examples": "{tr}sg @missrose_bot",
    },
)
async def _(event):  # sourcery no-metrics
    "To get name/username history."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "`Give userid or username to find name history`"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@SangMataInfo_bot"
    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(catevent, "`unblock @Sangmatainfo_bot and then try`")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(catevent, "`bot can't fetch results`")
    if "No records found" in responses:
        await edit_delete(catevent, "`The user doesn't have any record`")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    if cmd == "sg":
        sandy = None
        for i in names:
            if sandy:
                await event.reply(i, parse_mode=_format.parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=_format.parse_pre)
    elif cmd == "sgu":
        sandy = None
        for i in usernames:
            if sandy:
                await event.reply(i, parse_mode=_format.parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=_format.parse_pre)
