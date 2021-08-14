"""
created by @sandy1709
Idea by @BlazingRobonix
"""

from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import get_user_from_event

plugin_category = "fun"


@catub.cat_cmd(
    pattern="addecho$",
    command=("addecho", plugin_category),
    info={
        "header": "To repeat messages sent by the user.",
        "description": "Reply to user with this cmd so from then his every text and sticker messages will be repeated back to him.",
        "usage": "{tr}addecho <reply>",
    },
)
async def echo(event):
    "To echo the user messages"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "`Reply to a User's message to echo his messages`"
        )
    catevent = await edit_or_reply(event, "`Adding Echo to user...`")
    user, rank = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = get_display_name(await event.get_chat())
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "The user is already enabled with echo ")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"**Error:**\n`{e}`")
    else:
        await edit_or_reply(catevent, "Hi")


@catub.cat_cmd(
    pattern="rmecho$",
    command=("rmecho", plugin_category),
    info={
        "header": "To stop repeating paticular user messages.",
        "description": "Reply to user with this cmd to stop repeating his messages back.",
        "usage": "{tr}rmecho <reply>",
    },
)
async def echo(event):
    "To stop echoing the user messages"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "Reply to a User's message to echo his messages"
        )
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(catevent, f"**Error:**\n`{e}`")
        else:
            await edit_or_reply(event, "Echo has been stopped for the user")
    else:
        await edit_or_reply(event, "The user is not activated with echo")


@catub.cat_cmd(
    pattern="delecho( -a)?",
    command=("delecho", plugin_category),
    info={
        "header": "To delete echo in this chat.",
        "description": "To stop echoing users messages of all enabled users in the paticular chat or all chats.",
        "flags": {"a": "To stop in all chats"},
        "usage": [
            "{tr}delecho",
            "{tr}delecho -a",
        ],
    },
)
async def echo(event):
    "To delete echo in this chat."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "You havent enabled echo atleast for one user in any chat."
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "Deleted echo for all enabled users in all chats."
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "You havent enabled echo atleast for one user in this chat."
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{e}`", 10)
        else:
            await edit_or_reply(
                event, "Deleted echo for all enabled users in this chat"
            )


@catub.cat_cmd(
    pattern="listecho( -a)?$",
    command=("listecho", plugin_category),
    info={
        "header": "shows the list of users for whom you enabled echo",
        "flags": {
            "a": "To list echoed users in all chats",
        },
        "usage": [
            "{tr}listecho",
            "{tr}listecho -a",
        ],
    },
)
async def echo(event):  # sourcery no-metrics
    "To list all users on who you enabled echoing."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**Echo enabled users:**\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) <= 0:
            return await edit_or_reply(event, "There are no echo enabled users")
        for echos in lsts:
            if echos.chat_type == "Personal":
                if echos.user_username:
                    private_chats += (
                        f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    )
                else:
                    private_chats += (
                        f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                    )
            elif echos.user_username:
                group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"
            else:
                group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"

        if private_chats != "":
            output_str += "**Private Chats**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**Group Chats**\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(
                event, "There are no echo enabled users in this chat"
            )

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = "**Echo enabled users in this chat are:**\n" + private_chats

    await edit_or_reply(event, output_str)


@catub.cat_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
