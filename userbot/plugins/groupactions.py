from asyncio import sleep

from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageNotModifiedError,
    UserAdminInvalidError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBanned,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from telethon.utils import get_display_name

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import readable_time
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "admin"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


async def ban_user(chat_id, i, rights):
    try:
        await catub(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@catub.cat_cmd(
    pattern="kickme$",
    command=("kickme", plugin_category),
    info={
        "header": "To kick myself from group.",
        "usage": [
            "{tr}kickme",
        ],
    },
    groups_only=True,
)
async def kickme(leave):
    "to leave the group."
    await leave.edit("`Nope, no, no, I go away`")
    await leave.client.kick_participant(leave.chat_id, "me")


@catub.cat_cmd(
    pattern="kickall$",
    command=("kickall", plugin_category),
    info={
        "header": "To kick everyone from group.",
        "description": "To Kick all from the group except admins.",
        "usage": [
            "{tr}kickall",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To kick everyone from group."
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "`It seems like you dont have ban users permission in this group.`"
        )
    catevent = await edit_or_reply(event, "`Kicking...`")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await catevent.edit(
        f"`Sucessfully i have completed kickall process with {success} members kicked out of {total} members`"
    )


@catub.cat_cmd(
    pattern="banall$",
    command=("banall", plugin_category),
    info={
        "header": "To ban everyone from group.",
        "description": "To ban all from the group except admins.",
        "usage": [
            "{tr}kickall",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To ban everyone from group."
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "`It seems like you dont have ban users permission in this group.`"
        )
    catevent = await edit_or_reply(event, "`banning...`")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await catevent.edit(
        f"`Sucessfully i have completed banall process with {success} members banned out of {total} members`"
    )


@catub.cat_cmd(
    pattern="unbanall$",
    command=("unbanall", plugin_category),
    info={
        "header": "To unban all banned users from group.",
        "usage": [
            "{tr}unbanall",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To unban all banned users from group."
    catevent = await edit_or_reply(
        event, "__Unbanning all banned accounts in this group.__"
    )
    succ = 0
    total = 0
    flag = False
    await event.get_chat()
    async for i in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as e:
            LOGS.warn(f"A flood wait of {e.seconds} occurred.")
            await catevent.edit(
                f"__A wait of {readable_time(e.seconds)} needed again to continue the process.__"
            )
            await sleep(e.seconds + 5)
        except Exception as ex:
            await catevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await catevent.edit(
                        f"__Unbanning all banned accounts...,\n{succ} accounts are unbanned untill now.__"
                    )
            except MessageNotModifiedError:
                pass
    await catevent.edit(
        f"**Unbanned :**__{succ}/{total} in the chat {get_display_name(await event.get_chat())}__"
    )


# Ported by ©[NIKITA](t.me/kirito6969) and ©[EYEPATCH](t.me/NeoMatrix90)
@catub.cat_cmd(
    pattern="zombies( -r| )? ?([\s\S]*)",
    command=("zombies", plugin_category),
    info={
        "header": "To check deleted accounts and clean",
        "description": "Searches for deleted accounts in a group. Use `.zombies clean` to remove deleted accounts from the group.",
        "flag": {"-r": "Use this for check users from banned and restricted users"},
        "usage": [
            "{tr}zombies",
            "{tr}zombies clean",
            "{tr}zombies -r",
            "{tr}zombies -r clean",
        ],
    },
    groups_only=True,
)
async def rm_deletedacc(show):  # sourcery no-metrics
    "To check deleted accounts and clean"
    flag = show.pattern_match.group(1)
    con = show.pattern_match.group(2).lower()
    del_u = 0
    del_status = "`No zombies or deleted accounts found in this group, Group is clean`"
    if con != "clean":
        event = await edit_or_reply(
            show, "`Searching for ghost/deleted/zombie accounts...`"
        )
        if flag != " -r":
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    del_u += 1
            if del_u > 0:
                del_status = f"__Found__ **{del_u}** __ghost/deleted/zombie account(s) in this group,\
                            \nclean them by using__ `.zombies clean`"
        else:
            catadmin = await is_admin(show.client, show.chat_id, show.client.uid)
            if not catadmin:
                return await edit_delete(
                    event,
                    "`You must be admin to check zombies in restricted users`",
                    10,
                )
            async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBanned
            ):
                if user.deleted:
                    del_u += 1
            async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsKicked
            ):
                if user.deleted:
                    del_u += 1
            if del_u > 0:
                del_status = f"__Found__ **{del_u}** __ghost/deleted/zombie account(s) in this group who are restricted or banned,\
                            \nclean them by using__ `.zombies -r clean`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "`I am not an admin here!`", 5)
        return
    event = await edit_or_reply(
        show, "`Deleting deleted accounts...\nOh I can do that?!?!`"
    )
    del_u = 0
    del_a = 0
    if flag != " -r":
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                try:
                    await show.client.kick_participant(show.chat_id, user.id)
                    await sleep(0.5)
                    del_u += 1
                except ChatAdminRequiredError:
                    return await edit_delete(
                        event, "`I don't have ban rights in this group`", 5
                    )
                except FloodWaitError as e:
                    LOGS.warn(f"A flood wait of {e.seconds} occurred.")
                    await event.edit(
                        f"__A wait of {readable_time(e.seconds)} needed again to continue the process. Untill Now {del_u} users are cleaned.__"
                    )
                    await sleep(e.seconds + 5)
                    await event.edit(
                        f"__Ok the wait is over .I am cleaning all deleted accounts in this group__"
                    )
                except UserAdminInvalidError:
                    del_a += 1
                except Exception as e:
                    LOGS.error(str(e))
        if del_u > 0:
            del_status = (
                f"Successfully cleaned **{del_u}** deleted account(s) in the group."
            )
        if del_a > 0:
            del_status = f"Successfully cleaned **{del_u}** deleted account(s) in the group.\
            \n**{del_a}** deleted admin accounts are not removed"
    else:
        catadmin = await is_admin(show.client, show.chat_id, show.client.uid)
        if not catadmin:
            return await edit_delete(
                event, "`You must be admin to clean zombies in restricted users`", 10
            )
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsKicked
        ):
            if user.deleted:
                try:
                    await show.client.kick_participant(show.chat_id, user.id)
                    await sleep(0.5)
                    del_u += 1
                except ChatAdminRequiredError:
                    return await edit_delete(
                        event, "`I don't have ban rights in this group`", 5
                    )
                except FloodWaitError as e:
                    LOGS.warn(f"A flood wait of {e.seconds} occurred.")
                    await event.edit(
                        f"__A wait of {readable_time(e.seconds)} needed again to continue the process. Untill Now {del_u} users are cleaned.__"
                    )
                    await sleep(e.seconds + 5)
                    await event.edit(
                        f"__Ok the wait is over .I am cleaning all deleted accounts in restricted or banned users list in this group__"
                    )
                except Exception as e:
                    LOGS.error(str(e))
                    del_a += 1
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsBanned
        ):
            if user.deleted:
                try:
                    await show.client.kick_participant(show.chat_id, user.id)
                    await sleep(0.5)
                    del_u += 1
                except ChatAdminRequiredError:
                    return await edit_delete(
                        event, "`I don't have ban rights in this group`", 5
                    )
                except FloodWaitError as e:
                    LOGS.warn(f"A flood wait of {e.seconds} occurred.")
                    await event.edit(
                        f"__A wait of {readable_time(e.seconds)} needed again to continue the process. Untill Now {del_u} users are cleaned.__"
                    )
                    await sleep(e.seconds + 5)
                except Exception as e:
                    LOGS.error(str(e))
                    del_a += 1
        if del_u > 0:
            del_status = f"`Successfully cleaned {del_u} deleted account(s) in the group who are banned or restricted.`"
        if del_a > 0:
            del_status = f"`Successfully cleaned `**{del_u}**` deleted account(s) in the group who are banned or restricted.\
            \nFailed to kick `**{del_a}**` accounts.`"
    await edit_delete(event, del_status, 15)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#CLEANUP\
                \n{del_status}\
                \nCHAT: {get_display_name(await event.get_chat())}(`{show.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="ikuck ?([\s\S]*)",
    command=("ikuck", plugin_category),
    info={
        "header": "To get breif summary of members in the group",
        "description": "To get breif summary of members in the group . Need to add some features in future.",
        "usage": [
            "{tr}ikuck",
        ],
    },
    groups_only=True,
)
async def _(event):  # sourcery no-metrics
    "To get breif summary of members in the group.1 11"
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
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
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
        elif i.status is None:
            n += 1
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
        await sleep(5)
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
