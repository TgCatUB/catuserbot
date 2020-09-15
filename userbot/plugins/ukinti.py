""" @ukinti_bot
Available Commands:
.unbanall
.kick option
Available Options: d, y, m, w, o, q, r """
import asyncio
from time import sleep

from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="unbanall ?(.*)"))
@borg.on(sudo_cmd(pattern="unbanall ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "Searching Participant Lists.")
        p = 0
        async for i in borg.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await borg(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("{}: {} unbanned".format(event.chat_id, p))


@borg.on(admin_cmd(pattern="ikuck ?(.*)"))
@borg.on(sudo_cmd(pattern="ikuck (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await edit_or_reply(event, "`You aren't an admin here!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "Searching Participant Lists.")
    async for i in borg.iter_participants(event.chat_id):
        p = p + 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            q = q + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            r = r + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            b = b + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            d = d + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                else:
                    c = c + 1
        elif i.status is None:
            n = n + 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await et.edit(
        """Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


CMD_HELP.update(
    {
        "ukinti": "**Plugin : **`ukinti`\
        \n**Syntax : **`.unbanall`\
        \n**Usage: **Unbans everyone who are blocked in that group \
        \n\n**Syntax : **`.ikuck`\
        \n**Usage: **stats of the group like no of users no of deleted users. \
        "
    }
)
