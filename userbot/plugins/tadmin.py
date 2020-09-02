"""
idea from lynda and rose bot
made by @mrconfused
"""
from telethon.errors import (
    BadRequestError)
from telethon.errors.rpcerrorlist import (
    UserIdInvalidError)
from telethon.tl.functions.channels import (
    EditBannedRequest)
from telethon.tl.types import (
    ChatBannedRights,
    MessageEntityMentionName)
from userbot.utils import errors_handler, admin_cmd
from userbot.plugins import extract_time

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

# =================== CONSTANT ===================
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"
NO_SQL = "`Running on Non-SQL mode!`"


@borg.on(admin_cmd(pattern=r"tmute(?: |$)(.*)"))
@errors_handler
async def tmuter(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await catty.edit(NO_ADMIN)
        return
    user, reason = await get_user_from_event(catty)
    if user:
        pass
    else:
        return
    if reason:
        reason = reason.split(' ', 1)
        hmm = len(reason)
        if hmm == 2:
            cattime = reason[0]
            reason = reason[1]
        else:
            cattime = reason[0]
            reason = None
    else:
        await catty.edit("you havent mentioned time check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catty.edit(f"Invalid time type specified. Expected m , h , d or w not as {cattime}")
        return
    if user.id == self_user.id:
        await catty.edit(f"Sorry, I can't mute my self")
        return
    try:
        await catty.client(EditBannedRequest(catty.chat_id, user.id, ChatBannedRights(until_date=ctime, send_messages=True)))
        # Announce that the function is done
        if reason:
            await catty.edit(f"{user.first_name} was muted in {catty.chat.title}\n"f"Mutted until {cattime}\n"f"Reason:`{reason}`")
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID, "#TMUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {catty.chat.title}(`{catty.chat_id}`)\n"
                    f"MUTTED_UNTILL : `{cattime}`\n"
                    f"REASON : {reason}")
        else:
            await catty.edit(f"{user.first_name} was muted in {catty.chat.title}\n"f"Mutted until {cattime}\n")
            if BOTLOG:
                await catty.client.send_message(
                    BOTLOG_CHATID, "#TMUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {catty.chat.title}(`{catty.chat_id}`)\n"
                    f"MUTTED_UNTILL : `{cattime}`")
        # Announce to logging group
    except UserIdInvalidError:
        return await catty.edit("`Uh oh my mute logic broke!`")


@borg.on(admin_cmd(pattern=r"untmute(?: |$)(.*)"))
async def unmoot(catty):
    # Admin or creator check
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await catty.edit(NO_ADMIN)
        return
    # If admin or creator, inform the user and start unmuting
    await catty.edit('```Unmuting...```')
    user = await get_user_from_event(catty)
    user = user[0]
    if user:
        pass
    else:
        return
    try:
        await catty.client(EditBannedRequest(catty.chat_id, user.id, ChatBannedRights(until_date=None, send_messages=None)))
        await catty.edit("Unmuted Successfully")
    except UserIdInvalidError:
        await catty.edit("`Uh oh my unmute logic broke!`")
        return
    if BOTLOG:
        await catty.client.send_message(
            BOTLOG_CHATID, "#UNTMUTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {catty.chat.title}(`{catty.chat_id}`)")


@borg.on(admin_cmd("tban(?: |$)(.*)"))
@errors_handler
async def ban(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await catty.edit(NO_ADMIN)
        return
    user, reason = await get_user_from_event(catty)
    if user:
        pass
    else:
        return
    if reason:
        reason = reason.split(' ', 1)
        hmm = len(reason)
        if hmm == 2:
            cattime = reason[0]
            reason = reason[1]
        else:
            cattime = reason[0]
            reason = None
    else:
        await catty.edit("you havent mentioned time check `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catty.edit(f"Invalid time type specified. Expected m , h , d or w not as {cattime}")
        return
    if user.id == self_user.id:
        await catty.edit(f"Sorry, I can't ban my self")
        return
    await catty.edit("`Whacking the pest!`")
    try:
        await catty.client(EditBannedRequest(catty.chat_id, user.id,
                                             ChatBannedRights(until_date=ctime, view_messages=True)))
    except BadRequestError:
        await catty.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await catty.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catty.edit(
            "`I dont have message nuking rights! But still he was banned!`")
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await catty.edit(f"{user.first_name} was banned in {catty.chat.title}\n"f"banned until {cattime}\n"f"Reason:`{reason}`")
        if BOTLOG:
            await catty.client.send_message(
                BOTLOG_CHATID, "#TBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {catty.chat.title}(`{catty.chat_id}`)\n"
                f"BANNED_UNTILL : `{cattime}`\n"
                f"REASON : {reason}")
    else:
        await catty.edit(f"{user.first_name} was banned in {catty.chat.title}\n"f"banned until {cattime}\n")
        if BOTLOG:
            await catty.client.send_message(
                BOTLOG_CHATID, "#TBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {catty.chat.title}(`{catty.chat_id}`)\n"
                f"BANNED_UNTILL : `{cattime}`")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(' ', 1)
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
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
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
