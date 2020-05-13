import asyncio
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from userbot.utils import admin_cmd
import userbot.plugins.sql_helper.antiflood_sql as sql
import userbot.utils
from userbot.utils import humanbytes, progress, time_formatter
from userbot import CMD_HELP

CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True
)


@borg.on(admin_cmd(incoming=True))
async def _(event):
    # logger.info(CHAT_FLOOD)
    if not CHAT_FLOOD:
        return
    if not (str(event.chat_id) in CHAT_FLOOD):
        return
    # TODO: exempt admins from this
    should_ban = sql.update_flood(event.chat_id, event.message.from_id)
    if not should_ban:
        return
    try:
        await event.client(EditBannedRequest(
            event.chat_id,
            event.message.from_id,
            ANTI_FLOOD_WARN_MODE
        ))
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
@admin [User](tg://user?id={}) is flooding this chat.

`{}`""".format(event.message.from_id, str(e)),
            reply_to=event.message.id
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit(
            "This is useless SPAM dude . stop this enjoy chat man ",
            link_preview=False
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
[User](tg://user?id={}) has been automatically restricted
because he reached the defined flood limit.""".format(event.message.from_id),
            reply_to=event.message.id
        )


@borg.on(admin_cmd(pattern="setflood (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        sql.set_flood(event.chat_id, input_str)
        CHAT_FLOOD = sql.__load_flood_settings()
        await event.edit("Antiflood updated to {} in the current chat".format(input_str))
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))

        
CMD_HELP.update({
    "antiflood":
    ".setflood [number]\
\nUsage: warns the user if he spams the chat  if you are admin mutes him in that group .\
"
})              
