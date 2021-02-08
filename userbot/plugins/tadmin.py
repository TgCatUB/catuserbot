"""
idea from lynda and rose bot
made by @mrconfused
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

# =================== CONSTANT ===================
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"


@bot.on(admin_cmd(pattern=r"tmute(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"tmute(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def tmuter(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "`muting....`")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"Sorry, I can't mute myself")
        return
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


@bot.on(admin_cmd(pattern="tban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "`banning....`")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"Sorry, I can't ban myself")
        return
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
        await catevent.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await catty.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catevent.edit(
            "`I dont have message nuking rights! But still he was banned!`"
        )
        return
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


CMD_HELP.update(
    {
        "tadmin": "**Plugin :** `tadmin`\
      \n\n•  **Syntax : **`.tmute <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary mutes the user for given time.__\
      \n\n•  **Syntax : **`.tban <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary bans the user for given time.__\
      \n\n•  **Time units : ** __(2m = 2 minutes) ,(3h = 3hours)  ,(4d = 4 days) ,(5w = 5 weeks)\
      These times are example u can use anything with those units __"
    }
)
