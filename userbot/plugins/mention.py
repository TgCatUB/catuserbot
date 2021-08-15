from telethon.tl.types import ChannelParticipantsAdmins

from userbot import catub

from ..helpers.utils import get_user_from_event, reply_id

plugin_category = "extra"


@catub.cat_cmd(
    pattern="(tagall|all)(?:\s|$)([\s\S]*)",
    command=("tagall", plugin_category),
    info={
        "header": "tags recent 50 persons in the group may not work for all",
        "usage": [
            "{tr}all <text>",
            "{tr}tagall",
        ],
    },
)
async def _(event):
    "To tag all."
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(2)
    mentions = input_str or "@all"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 50):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@catub.cat_cmd(
    pattern="report$",
    command=("report", plugin_category),
    info={
        "header": "To tags admins in group.",
        "usage": "{tr}report",
    },
)
async def _(event):
    "To tags admins in group."
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    reply_to_id = await reply_id(event)
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@catub.cat_cmd(
    pattern="men ([\s\S]*)",
    command=("mention", plugin_category),
    info={
        "header": "Tags that person with the given custom text.",
        "usage": [
            "{tr}men username/userid text",
            "text (username/mention)[custom text] text",
        ],
        "examples": ["{tr}men @mrconfused hi", "Hi @mrconfused[How are you?]"],
    },
)
async def _(event):
    "Tags that person with the given custom text."
    user, input_str = await get_user_from_event(event)
    if not user:
        return
    reply_to_id = await reply_id(event)
    await event.delete()
    await event.client.send_message(
        event.chat_id,
        f"<a href='tg://user?id={user.id}'>{input_str}</a>",
        parse_mode="HTML",
        reply_to=reply_to_id,
    )
