# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import types
from telethon.tl.functions.contacts import UnblockRequest as unblock

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _format, sanga_seperator
from ..helpers.utils import _format

plugin_category = "utils"


@catub.cat_cmd(
    pattern="sg(|u)(?:\s|$)([\s\S]*)",
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
async def sangmata(event):
    "To get name/username history."
    cmd = event.pattern_match.group(1)
    user = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not user and reply:
        user = reply.from_id
    if not user:
        return await edit_delete(
            event,
            "`Reply to  user's text message to get name/username history or give userid/username`",
        )

    userinfo = await catub.get_entity(user)
    if not isinstance(userinfo, types.User):
        return await edit_delete(event, "`Can't fetch the user...`")

    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation("@SangMata_beta_bot") as conv:
        try:
            await conv.send_message(userinfo.id)
        except YouBlockedUserError:
            await catub(unblock("SangMata_beta_bot"))
            await conv.send_message(userinfo.id)
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)

    if not responses:
        await edit_delete(catevent, "`Bot can't fetch results`")
    if "No records found" in responses:
        await edit_delete(catevent, "`The user doesn't have any record`")

    names, usernames = sanga_seperator(responses)
    check = (usernames, "Username") if cmd == "u" else (names, "Name")
    user_name = (
        f"{userinfo.first_name} {userinfo.last_name}"
        if userinfo.last_name
        else userinfo.first_name
    )
    output = f"**➜ User Info :**  {_format.mentionuser(user_name, userinfo.id)}\n**➜ {check[1]} History :**\n{check[0]}"
    await edit_or_reply(catevent, output)
