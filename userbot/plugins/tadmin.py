"""
idea from lynda and rose bot
made by @mrconfused
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, MessageEntityMentionName

from ..utils import admin_cmd, edit_or_reply, errors_handler, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, extract_time

# =================== CONSTANT ===================
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"


@borg.on(admin_cmd(pattern=r"tmute(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern=r"tmute(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def tmuter(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "`muteing....`")
    user, reason = await get_user_from_event(catty)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("you havent mentioned time check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"Sorry, I can't mute my self")
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
                f"{user.first_name} was muted in {catty.chat.title}\n"
                f"**Mutted for : **{cattime}\n"
                f"**Reason : **__{reason}__"
            )
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                    f"**Mutted for : **`{cattime}`\n"
                    f"**Reason : **`{reason}``",
                )
        else:
            await catevent.edit(
                f"{user.first_name} was muted in {catty.chat.title}\n"
                f"Mutted for {cattime}\n"
            )
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{catty.chat.title}(`{catty.chat_id}`)\n"
                    f"**Mutted for : **`{cattime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await catevent.edit("`Uh oh my mute logic broke!`")


@borg.on(admin_cmd(pattern="tban(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="tban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "`baning....`")
    user, reason = await get_user_from_event(catty)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("you havent mentioned time check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"Sorry, I can't ban my self")
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
            f"{user.first_name} was banned in {catty.chat.title}\n"
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
            f"{user.first_name} was banned in {catty.chat.title}\n"
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


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Could not fetch info of that user.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CMD_HELP.update(
    {
        "tadmin": "**Plugin :** `tadmin`\
      \n\n**Syntax : **`.tmute <reply/username/userid> <time> <reason>`\
      \n**Usage : **Temporary mutes the user for given time.\
      \n\n**Syntax : **`.tban <reply/username/userid> <time> <reason>`\
      \n**Usage : **Temporary bans the user for given time.\
      \n\n**Time units : ** (2m = 2 minutes) ,(3h = 3hours)  ,(4d = 4 days) ,(5w = 5 weeks)\
      This times are example u can use anything with thoose untis "
    }
)
