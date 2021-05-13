"""
idea from lynda and rose bot
made by @mrconfused
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import (UserAdminInvalidError,
                                          UserIdInvalidError)
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

plugin_category = "admin"

# =================== CONSTANT ===================
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"


@catub.cat_cmd(
    pattern="tmute(?: |$)(.*)",
    command=("tmute", plugin_category),
    info={
        "header": "To stop sending messages permission for that user",
        "description": "Temporary mutes the user for given time.",
        "Time units": {
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tmute <userid/username/reply> <time>",
            "{tr}tmute <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tmute 2d to test muting for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tmuter(catty):
    "To mute a person for specific time"
    catevent = await edit_or_reply(catty, "`muting....`")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit("you haven't mentioned time, check `.help tmute`")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0]
    reason = reason[1] if hmm == 2 else None
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        return await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
    if user.id == self_user.id:
        return await catevent.edit(f"Sorry, I can't mute myself")
    try:
        await catevent.client(
            EditBannedRequest(
                catty.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await catevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {catty.chat.title}\n"
                f"**Muted for : **{cattime}\n"
                f"**Reason : **__{reason}__"
            )
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                    f"**Muted for : **`{cattime}`\n"
                    f"**Reason : **`{reason}``",
                )
        else:
            await catevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {catty.chat.title}\n"
                f"Muted for {cattime}\n"
            )
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                    f"**Muted for : **`{cattime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await catevent.edit("`Uh oh my mute logic broke!`")
    except UserAdminInvalidError:
        return await catevent.edit(
            "`Either you're not an admin or you tried to mute an admin that you didn't promote`"
        )
    except Exception as e:
        return await catevent.edit(f"`{str(e)}`")


@catub.cat_cmd(
    pattern="tban(?: |$)(.*)",
    command=("tban", plugin_category),
    info={
        "header": "To remove a user from the group for specified time.",
        "description": "Temporary bans the user for given time.",
        "Time units": {
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tban <userid/username/reply> <time>",
            "{tr}tban <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tban 2d to test baning for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tban(catty):  # sourcery no-metrics
    "To ban a person for specific time"
    catevent = await edit_or_reply(catty, "`banning....`")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit("you haven't mentioned time, check `.help tban`")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0]
    reason = reason[1] if hmm == 2 else None
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        return await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
    if user.id == self_user.id:
        return await catevent.edit(f"Sorry, I can't ban myself")
    await catevent.edit("`Whacking the pest!`")
    try:
        await catty.client(
            EditBannedRequest(
                catty.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await catevent.edit(
            "`Either you're not an admin or you tried to ban an admin that you didn't promote`"
        )
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await catty.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "`I dont have message nuking rights! But still he was banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {catty.chat.title}\n"
            f"banned for {cattime}\n"
            f"Reason:`{reason}`"
        )
        if BOTLOG:
            await catty.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                f"**Banned untill : **`{cattime}`\n"
                f"**Reason : **__{reason}__",
            )
    else:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {catty.chat.title}\n"
            f"banned for {cattime}\n"
        )
        if BOTLOG:
            await catty.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                f"**Banned untill : **`{cattime}`",
            )
