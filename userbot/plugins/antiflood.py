import asyncio

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

import userbot.plugins.sql_helper.antiflood_sql as sql

CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@bot.on(admin_cmd(incoming=True))
async def _(event):
    if not CHAT_FLOOD:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
@admin [User](tg://user?id={}) is flooding this chat.
`{}`""".format(
                event.message.sender_id, str(e)
            ),
            reply_to=event.message.id,
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit(
            "This is useless SPAM dude. Stop this, enjoy chat man ", link_preview=False
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
[User](tg://user?id={}) has been automatically restricted
because he reached the defined flood limit.""".format(
                event.message.sender_id
            ),
            reply_to=event.message.id,
        )


@bot.on(admin_cmd(pattern="setflood(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="setflood(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "updating flood settings!")
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(
            "Antiflood updated to {} in the current chat".format(input_str)
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


CMD_HELP.update(
    {
        "antiflood": ".setflood [number]\
\nUsage: warns the user if he spams the chat and if you are an admin then it mutes him in that group.\
"
    }
)
