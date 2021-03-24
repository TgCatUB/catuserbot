import base64

from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights

from ..utils import is_admin
from . import BOTLOG, get_user_from_event
from .sql_helper.locks_sql import get_locks, is_locked, update_lock


@bot.on(admin_cmd(pattern=r"lock (.*)"))
@bot.on(sudo_cmd(pattern=r"lock (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "`Idiot! ,This is not a group to lock things `")
    chat_per = (await event.get_chat()).default_banned_rights
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await edit_or_reply(event, "`Locked {}`".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        embed_link = chat_per.embed_links
        gpoll = chat_per.send_polls
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "msg":
            if msg:
                return await edit_delete(
                    event, "`This group is already locked with messaging permission`"
                )
            msg = True
            locktype = "messages"
        elif input_str == "media":
            if media:
                return await edit_delete(
                    event, "`This group is already locked with sending media`"
                )
            media = True
            locktype = "media"
        elif input_str == "sticker":
            if sticker:
                return await edit_delete(
                    event, "`This group is already locked with sending stickers`"
                )
            sticker = True
            locktype = "stickers"
        elif input_str == "preview":
            if embed_link:
                return await edit_delete(
                    event, "`This group is already locked with previewing links`"
                )
            embed_link = True
            locktype = "preview links"
        elif input_str == "gif":
            if gif:
                return await edit_delete(
                    event, "`This group is already locked with sending GIFs`"
                )
            gif = True
            locktype = "GIFs"
        elif input_str == "game":
            if gamee:
                return await edit_delete(
                    event, "`This group is already locked with sending games`"
                )
            gamee = True
            locktype = "games"
        elif input_str == "inline":
            if ainline:
                return await edit_delete(
                    event, "`This group is already locked with using inline bots`"
                )
            ainline = True
            locktype = "inline bots"
        elif input_str == "poll":
            if gpoll:
                return await edit_delete(
                    event, "`This group is already locked with sending polls`"
                )
            gpoll = True
            locktype = "polls"
        elif input_str == "invite":
            if adduser:
                return await edit_delete(
                    event, "`This group is already locked with adding members`"
                )
            adduser = True
            locktype = "invites"
        elif input_str == "pin":
            if cpin:
                return await edit_delete(
                    event,
                    "`This group is already locked with pinning messages by users`",
                )
            cpin = True
            locktype = "pins"
        elif input_str == "info":
            if changeinfo:
                return await edit_delete(
                    event,
                    "`This group is already locked with Changing group info by users`",
                )
            changeinfo = True
            locktype = "chat info"
        elif input_str == "all":
            msg = True
            media = True
            sticker = True
            gif = True
            gamee = True
            ainline = True
            embed_link = True
            gpoll = True
            adduser = True
            cpin = True
            changeinfo = True
            locktype = "everything"
        else:
            if input_str:
                return await edit_delete(
                    event, f"**Invalid lock type :** `{input_str}`", time=5
                )

            return await edit_or_reply(event, "`I can't lock nothing !!`")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        lock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            embed_links=embed_link,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(
                EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=lock_rights
                )
            )
            await edit_or_reply(event, f"`Locked {locktype} for this chat !!`")
        except BaseException as e:
            await edit_delete(
                event,
                f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
                time=5,
            )


@bot.on(admin_cmd(pattern="unlock (.*)"))
@bot.on(sudo_cmd(pattern="unlock (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "`Idiot! ,This is not a group to lock things `")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await edit_or_reply(event, "`UnLocked {}`".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        gpoll = chat_per.send_polls
        embed_link = chat_per.embed_links
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "msg":
            if not msg:
                return await edit_delete(
                    event, "`This group is already unlocked with messaging permission`"
                )
            msg = False
            locktype = "messages"
        elif input_str == "media":
            if not media:
                return await edit_delete(
                    event, "`This group is already unlocked with sending media`"
                )
            media = False
            locktype = "media"
        elif input_str == "sticker":
            if not sticker:
                return await edit_delete(
                    event, "`This group is already unlocked with sending stickers`"
                )
            sticker = False
            locktype = "stickers"
        elif input_str == "preview":
            if not embed_link:
                return await edit_delete(
                    event, "`This group is already unlocked with preview links`"
                )
            embed_link = False
            locktype = "preview links"
        elif input_str == "gif":
            if not gif:
                return await edit_delete(
                    event, "`This group is already unlocked with sending GIFs`"
                )
            gif = False
            locktype = "GIFs"
        elif input_str == "game":
            if not gamee:
                return await edit_delete(
                    event, "`This group is already unlocked with sending games`"
                )
            gamee = False
            locktype = "games"
        elif input_str == "inline":
            if not ainline:
                return await edit_delete(
                    event, "`This group is already unlocked with using inline bots`"
                )
            ainline = False
            locktype = "inline bots"
        elif input_str == "poll":
            if not gpoll:
                return await edit_delete(
                    event, "`This group is already unlocked with sending polls`"
                )
            gpoll = False
            locktype = "polls"
        elif input_str == "invite":
            if not adduser:
                return await edit_delete(
                    event, "`This group is already unlocked with adding members`"
                )
            adduser = False
            locktype = "invites"
        elif input_str == "pin":
            if not cpin:
                return await edit_delete(
                    event,
                    "`This group is already unlocked with pinning messages by users`",
                )
            cpin = False
            locktype = "pins"
        elif input_str == "info":
            if not changeinfo:
                return await edit_delete(
                    event,
                    "`This group is already unlocked with Changing grup info by users`",
                )
            changeinfo = False
            locktype = "chat info"
        elif input_str == "all":
            msg = False
            media = False
            sticker = False
            gif = False
            gamee = False
            ainline = False
            gpoll = False
            embed_link = False
            adduser = False
            cpin = False
            changeinfo = False
            locktype = "everything"
        else:
            if input_str:
                return await edit_delete(
                    event, f"**Invalid unlock type :** `{input_str}`", time=5
                )

            return await edit_or_reply(event, "`I can't unlock nothing !!`")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        unlock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            embed_links=embed_link,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(
                EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=unlock_rights
                )
            )
            await edit_or_reply(event, f"`Unlocked {locktype} for this chat !!`")
        except BaseException as e:
            return await edit_delete(
                event,
                f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
                time=5,
            )


@bot.on(admin_cmd(pattern="locks$"))
@bot.on(sudo_cmd(pattern="locks$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "There are no DataBase settings in this chat"
    else:
        res = "Following are the DataBase permissions in this chat: \n"
        ubots = "❌" if current_db_locks.bots else "✅"
        ucommands = "❌" if current_db_locks.commands else "✅"
        uemail = "❌" if current_db_locks.email else "✅"
        uforward = "❌" if current_db_locks.forward else "✅"
        uurl = "❌" if current_db_locks.url else "✅"
        res += f"👉 `bots`: `{ubots}`\n"
        res += f"👉 `commands`: `{ucommands}`\n"
        res += f"👉 `email`: `{uemail}`\n"
        res += f"👉 `forward`: `{uforward}`\n"
        res += f"👉 `url`: `{uurl}`\n"
    current_chat = await event.get_chat()
    try:
        chat_per = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        umsg = "❌" if chat_per.send_messages else "✅"
        umedia = "❌" if chat_per.send_media else "✅"
        usticker = "❌" if chat_per.send_stickers else "✅"
        ugif = "❌" if chat_per.send_gifs else "✅"
        ugamee = "❌" if chat_per.send_games else "✅"
        uainline = "❌" if chat_per.send_inline else "✅"
        uembed_link = "❌" if chat_per.embed_links else "✅"
        ugpoll = "❌" if chat_per.send_polls else "✅"
        uadduser = "❌" if chat_per.invite_users else "✅"
        ucpin = "❌" if chat_per.pin_messages else "✅"
        uchangeinfo = "❌" if chat_per.change_info else "✅"
        res += "\nThis are current permissions of this chat: \n"
        res += f"👉 `msg`: `{umsg}`\n"
        res += f"👉 `media`: `{umedia}`\n"
        res += f"👉 `sticker`: `{usticker}`\n"
        res += f"👉 `gif`: `{ugif}`\n"
        res += f"👉 `preview`: `{uembed_link}`\n"
        res += f"👉 `gamee`: `{ugamee}`\n"
        res += f"👉 `ainline`: `{uainline}`\n"
        res += f"👉 `gpoll`: `{ugpoll}`\n"
        res += f"👉 `adduser`: `{uadduser}`\n"
        res += f"👉 `cpin`: `{ucpin}`\n"
        res += f"👉 `changeinfo`: `{uchangeinfo}`\n"
    await edit_or_reply(event, res)


@bot.on(admin_cmd(pattern=r"plock (.*)"))
@bot.on(sudo_cmd(pattern=r"plock (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    reply = await event.get_reply_message()
    if not event.is_group:
        return await edit_delete(event, "`Idiot! ,This is not a group to lock things `")
    chat_per = (await event.get_chat()).default_banned_rights
    result = await event.client(
        functions.channels.GetParticipantRequest(channel=peer_id, user_id=reply.from_id)
    )
    admincheck = await is_admin(event.client, peer_id, reply.from_id)
    if admincheck:
        return await edit_delete(event, "`This user is admin you cant play with him`")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    msg = chat_per.send_messages
    media = chat_per.send_media
    sticker = chat_per.send_stickers
    gif = chat_per.send_gifs
    gamee = chat_per.send_games
    ainline = chat_per.send_inline
    embed_link = chat_per.embed_links
    gpoll = chat_per.send_polls
    adduser = chat_per.invite_users
    cpin = chat_per.pin_messages
    changeinfo = chat_per.change_info
    try:
        umsg = result.participant.banned_rights.send_messages
        umedia = result.participant.banned_rights.send_media
        usticker = result.participant.banned_rights.send_stickers
        ugif = result.participant.banned_rights.send_gifs
        ugamee = result.participant.banned_rights.send_games
        uainline = result.participant.banned_rights.send_inline
        uembed_link = result.participant.banned_rights.embed_links
        ugpoll = result.participant.banned_rights.send_polls
        uadduser = result.participant.banned_rights.invite_users
        ucpin = result.participant.banned_rights.pin_messages
        uchangeinfo = result.participant.banned_rights.change_info
    except AttributeError:
        umsg = msg
        umedia = media
        usticker = sticker
        ugif = gif
        ugamee = gamee
        uainline = ainline
        uembed_link = embed_link
        ugpoll = gpoll
        uadduser = adduser
        ucpin = cpin
        uchangeinfo = changeinfo
    if input_str == "msg":
        if msg:
            return await edit_delete(
                event, "`This Group is already locked with messaging permission.`"
            )
        if umsg:
            return await edit_delete(
                event, "`This User is already locked with messaging permission.`"
            )
        umsg = True
        locktype = "messages"
    elif input_str == "media":
        if media:
            return await edit_delete(
                event, "`This group is already locked with sending media`"
            )
        if umedia:
            return await edit_delete(
                event, "`User is already locked with sending media`"
            )
        umedia = True
        locktype = "media"
    elif input_str == "sticker":
        if sticker:
            return await edit_delete(
                event, "`This group is already locked with sending stickers`"
            )
        if usticker:
            return await edit_delete(
                event, "`This user is already locked with sending stickers`"
            )
        usticker = True
        locktype = "stickers"
    elif input_str == "preview":
        if embed_link:
            return await edit_delete(
                event, "`This group is already locked with previewing links`"
            )
        if uembed_link:
            return await edit_delete(
                event, "`This group is already locked with previewing links`"
            )
        uembed_link = True
        locktype = "preview links"
    elif input_str == "gif":
        if gif:
            return await edit_delete(
                event, "`This group is already locked with sending GIFs`"
            )
        if ugif:
            return await edit_delete(
                event, "`This user is already locked with sending GIFs`"
            )
        ugif = True
        locktype = "GIFs"
    elif input_str == "game":
        if gamee:
            return await edit_delete(
                event, "`This group is already locked with sending games`"
            )
        if ugamee:
            return await edit_delete(
                event, "`This user is already locked with sending games`"
            )
        ugamee = True
        locktype = "games"
    elif input_str == "inline":
        if ainline:
            return await edit_delete(
                event, "`This group is already locked with using inline bots`"
            )
        if uainline:
            return await edit_delete(
                event, "`This user is already locked with using inline bots`"
            )
        uainline = True
        locktype = "inline bots"
    elif input_str == "poll":
        if gpoll:
            return await edit_delete(
                event, "`This group is already locked with sending polls`"
            )
        if ugpoll:
            return await edit_delete(
                event, "`This user is already locked with sending polls`"
            )
        ugpoll = True
        locktype = "polls"
    elif input_str == "invite":
        if adduser:
            return await edit_delete(
                event, "`This group is already locked with adding members`"
            )
        if uadduser:
            return await edit_delete(
                event, "`This user is already locked with adding members`"
            )
        uadduser = True
        locktype = "invites"
    elif input_str == "pin":
        if cpin:
            return await edit_delete(
                event,
                "`This group is already locked with pinning messages by users`",
            )
        if ucpin:
            return await edit_delete(
                event,
                "`This user is already locked with pinning messages by users`",
            )
        ucpin = True
        locktype = "pins"
    elif input_str == "info":
        if changeinfo:
            return await edit_delete(
                event,
                "`This group is already locked with Changing group info by users`",
            )
        if uchangeinfo:
            return await edit_delete(
                event,
                "`This user is already locked with Changing group info by users`",
            )
        uchangeinfo = True
        locktype = "chat info"
    elif input_str == "all":
        umsg = True
        umedia = True
        usticker = True
        ugif = True
        ugamee = True
        uainline = True
        uembed_link = True
        ugpoll = True
        uadduser = True
        ucpin = True
        uchangeinfo = True
        locktype = "everything"
    else:
        if input_str:
            return await edit_delete(
                event, f"**Invalid lock type :** `{input_str}`", time=5
            )

        return await edit_or_reply(event, "`I can't lock nothing !!`")
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=umsg,
        send_media=umedia,
        send_stickers=usticker,
        send_gifs=ugif,
        send_games=ugamee,
        send_inline=uainline,
        embed_links=uembed_link,
        send_polls=ugpoll,
        invite_users=uadduser,
        pin_messages=ucpin,
        change_info=uchangeinfo,
    )
    try:
        await event.client(EditBannedRequest(peer_id, reply.from_id, lock_rights))
        await edit_or_reply(event, f"`Locked {locktype} for this user !!`")
    except BaseException as e:
        await edit_delete(
            event,
            f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
            time=5,
        )


@bot.on(admin_cmd(pattern=r"punlock (.*)"))
@bot.on(sudo_cmd(pattern=r"punlock (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    reply = await event.get_reply_message()
    if not event.is_group:
        return await edit_delete(event, "`Idiot! ,This is not a group to lock things `")
    chat_per = (await event.get_chat()).default_banned_rights
    result = await event.client(
        functions.channels.GetParticipantRequest(channel=peer_id, user_id=reply.from_id)
    )
    admincheck = await is_admin(event.client, peer_id, reply.from_id)
    if admincheck:
        return await edit_delete(event, "`This user is admin you cant play with him`")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    msg = chat_per.send_messages
    media = chat_per.send_media
    sticker = chat_per.send_stickers
    gif = chat_per.send_gifs
    gamee = chat_per.send_games
    ainline = chat_per.send_inline
    embed_link = chat_per.embed_links
    gpoll = chat_per.send_polls
    adduser = chat_per.invite_users
    cpin = chat_per.pin_messages
    changeinfo = chat_per.change_info
    try:
        umsg = result.participant.banned_rights.send_messages
        umedia = result.participant.banned_rights.send_media
        usticker = result.participant.banned_rights.send_stickers
        ugif = result.participant.banned_rights.send_gifs
        ugamee = result.participant.banned_rights.send_games
        uainline = result.participant.banned_rights.send_inline
        uembed_link = result.participant.banned_rights.embed_links
        ugpoll = result.participant.banned_rights.send_polls
        uadduser = result.participant.banned_rights.invite_users
        ucpin = result.participant.banned_rights.pin_messages
        uchangeinfo = result.participant.banned_rights.change_info
    except AttributeError:
        umsg = msg
        umedia = media
        usticker = sticker
        ugif = gif
        ugamee = gamee
        uainline = ainline
        uembed_link = embed_link
        ugpoll = gpoll
        uadduser = adduser
        ucpin = cpin
        uchangeinfo = changeinfo
    if input_str == "msg":
        if msg:
            return await edit_delete(
                event, "`This Group is locked with messaging permission.`"
            )
        if not umsg:
            return await edit_delete(
                event, "`This User is already unlocked with messaging permission.`"
            )
        umsg = False
        locktype = "messages"
    elif input_str == "media":
        if media:
            return await edit_delete(event, "`This Group is locked with sending media`")
        if not umedia:
            return await edit_delete(
                event, "`User is already unlocked with sending media`"
            )
        umedia = False
        locktype = "media"
    elif input_str == "sticker":
        if sticker:
            return await edit_delete(
                event, "`This Group is locked with sending stickers`"
            )
        if not usticker:
            return await edit_delete(
                event, "`This user is already unlocked with sending stickers`"
            )
        usticker = False
        locktype = "stickers"
    elif input_str == "preview":
        if embed_link:
            return await edit_delete(
                event, "`This Group is locked with previewing links`"
            )
        if not uembed_link:
            return await edit_delete(
                event, "`This user is already unlocked with previewing links`"
            )
        uembed_link = False
        locktype = "preview links"
    elif input_str == "gif":
        if gif:
            return await edit_delete(event, "`This Group is locked with sending GIFs`")
        if not ugif:
            return await edit_delete(
                event, "`This user is already unlocked with sending GIFs`"
            )
        ugif = False
        locktype = "GIFs"
    elif input_str == "game":
        if gamee:
            return await edit_delete(event, "`This Group is locked with sending games`")
        if not ugamee:
            return await edit_delete(
                event, "`This user is already unlocked with sending games`"
            )
        ugamee = False
        locktype = "games"
    elif input_str == "inline":
        if ainline:
            return await edit_delete(
                event, "`This Group is locked with using inline bots`"
            )
        if not uainline:
            return await edit_delete(
                event, "`This user is already unlocked with using inline bots`"
            )
        uainline = False
        locktype = "inline bots"
    elif input_str == "poll":
        if gpoll:
            return await edit_delete(event, "`This Group is locked with sending polls`")
        if not ugpoll:
            return await edit_delete(
                event, "`This user is already unlocked with sending polls`"
            )
        ugpoll = False
        locktype = "polls"
    elif input_str == "invite":
        if adduser:
            return await edit_delete(
                event, "`This Group is locked with adding members`"
            )
        if not uadduser:
            return await edit_delete(
                event, "`This user is already unlocked with adding members`"
            )
        uadduser = False
        locktype = "invites"
    elif input_str == "pin":
        if cpin:
            return await edit_delete(
                event,
                "`This Group is locked with pinning messages by users`",
            )
        if not ucpin:
            return await edit_delete(
                event,
                "`This user is already unlocked with pinning messages by users`",
            )
        ucpin = False
        locktype = "pins"
    elif input_str == "info":
        if changeinfo:
            return await edit_delete(
                event,
                "`This Group is locked with Changing group info by users`",
            )
        if not uchangeinfo:
            return await edit_delete(
                event,
                "`This user is already unlocked with Changing group info by users`",
            )
        uchangeinfo = False
        locktype = "chat info"
    elif input_str == "all":
        if not msg:
            umsg = False
        if not media:
            umedia = False
        if not sticker:
            usticker = False
        if not gif:
            ugif = False
        if not gamee:
            ugamee = False
        if not ainline:
            uainline = False
        if not embed_link:
            uembed_link = False
        if not gpoll:
            ugpoll = False
        if not adduser:
            uadduser = False
        if not cpin:
            ucpin = False
        if not changeinfo:
            uchangeinfo = False
        locktype = "everything"
    else:
        if input_str:
            return await edit_delete(
                event, f"**Invalid lock type :** `{input_str}`", time=5
            )

        return await edit_or_reply(event, "`I can't lock nothing !!`")
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=umsg,
        send_media=umedia,
        send_stickers=usticker,
        send_gifs=ugif,
        send_games=ugamee,
        send_inline=uainline,
        embed_links=uembed_link,
        send_polls=ugpoll,
        invite_users=uadduser,
        pin_messages=ucpin,
        change_info=uchangeinfo,
    )
    try:
        await event.client(EditBannedRequest(peer_id, reply.from_id, lock_rights))
        await edit_or_reply(event, f"`Unlocked {locktype} for this user !!`")
    except BaseException as e:
        await edit_delete(
            event,
            f"`Do I have proper rights for that ??`\n\n**Error:** `{str(e)}`",
            time=5,
        )


@bot.on(admin_cmd(pattern="uperm(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="uperm(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    peer_id = event.chat_id
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if not event.is_group:
        return await edit_delete(event, "`Idiot! ,This is not a group to lock things `")
    admincheck = await is_admin(event.client, peer_id, user.id)
    result = await event.client(
        functions.channels.GetParticipantRequest(channel=peer_id, user_id=user.id)
    )
    output = ""
    if admincheck:
        c_info = "✅" if result.participant.admin_rights.change_info else "❌"
        del_me = "✅" if result.participant.admin_rights.delete_messages else "❌"
        ban = "✅" if result.participant.admin_rights.ban_users else "❌"
        invite_u = "✅" if result.participant.admin_rights.invite_users else "❌"
        pin = "✅" if result.participant.admin_rights.pin_messages else "❌"
        add_a = "✅" if result.participant.admin_rights.add_admins else "❌"
        call = "✅" if result.participant.admin_rights.manage_call else "❌"
        output += f"**Admin rights of **{_format.mentionuser(user.first_name ,user.id)} **in {event.chat.title} chat are **\n"
        output += f"__Change info :__ {c_info}\n"
        output += f"__Delete messages :__ {del_me}\n"
        output += f"__Ban users :__ {ban}\n"
        output += f"__Invite users :__ {invite_u}\n"
        output += f"__Pin messages :__ {pin}\n"
        output += f"__Add admins :__ {add_a}\n"
        output += f"__Manage call :__ {call}\n"
    else:
        chat_per = (await event.get_chat()).default_banned_rights
        try:
            umsg = "❌" if result.participant.banned_rights.send_messages else "✅"
            umedia = "❌" if result.participant.banned_rights.send_media else "✅"
            usticker = "❌" if result.participant.banned_rights.send_stickers else "✅"
            ugif = "❌" if result.participant.banned_rights.send_gifs else "✅"
            ugamee = "❌" if result.participant.banned_rights.send_games else "✅"
            uainline = "❌" if result.participant.banned_rights.send_inline else "✅"
            uembed_link = "❌" if result.participant.banned_rights.embed_links else "✅"
            ugpoll = "❌" if result.participant.banned_rights.send_polls else "✅"
            uadduser = "❌" if result.participant.banned_rights.invite_users else "✅"
            ucpin = "❌" if result.participant.banned_rights.pin_messages else "✅"
            uchangeinfo = "❌" if result.participant.banned_rights.change_info else "✅"
        except AttributeError:
            umsg = "❌" if chat_per.send_messages else "✅"
            umedia = "❌" if chat_per.send_media else "✅"
            usticker = "❌" if chat_per.send_stickers else "✅"
            ugif = "❌" if chat_per.send_gifs else "✅"
            ugamee = "❌" if chat_per.send_games else "✅"
            uainline = "❌" if chat_per.send_inline else "✅"
            uembed_link = "❌" if chat_per.embed_links else "✅"
            ugpoll = "❌" if chat_per.send_polls else "✅"
            uadduser = "❌" if chat_per.invite_users else "✅"
            ucpin = "❌" if chat_per.pin_messages else "✅"
            uchangeinfo = "❌" if chat_per.change_info else "✅"
        output += f"{_format.mentionuser(user.first_name ,user.id)} **permissions in {event.chat.title} chat are **\n"
        output += f"__Send Messages :__ {umsg}\n"
        output += f"__Send Media :__ {umedia}\n"
        output += f"__Send Stickers :__ {usticker}\n"
        output += f"__Send Gifs :__ {ugif}\n"
        output += f"__Send Games :__ {ugamee}\n"
        output += f"__Send Inline bots :__ {uainline}\n"
        output += f"__Send Polls :__ {ugpoll}\n"
        output += f"__Embed links :__ {uembed_link}\n"
        output += f"__Add Users :__ {uadduser}\n"
        output += f"__Pin messages :__ {ucpin}\n"
        output += f"__Change Chat Info :__ {uchangeinfo}\n"
    await edit_or_reply(event, output)


@bot.on(events.MessageEdited())
@bot.on(events.NewMessage())
async def check_incoming_messages(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    peer_id = event.chat_id
    if is_locked(peer_id, "commands"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "commands", False)
    if is_locked(peer_id, "forward") and event.fwd_from:
        try:
            await event.delete()
        except Exception as e:
            await event.reply(
                "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
            )
            update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "email"):
        entities = event.message.entities
        is_email = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "email", False)
    if is_locked(peer_id, "url"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(
                    entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)
                ):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "I don't seem to have ADMIN permission here. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)


@bot.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    # check for "lock" "bots"
    if not is_locked(event.chat_id, "bots"):
        return
    # bots are limited Telegram accounts,
    # and cannot join by themselves
    if event.user_added:
        users_added_by = event.action_message.sender_id
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                try:
                    await event.client(
                        functions.channels.EditBannedRequest(
                            event.chat_id, user_obj, rights
                        )
                    )
                except Exception as e:
                    await event.reply(
                        "I don't seem to have ADMIN permission here. \n`{}`".format(
                            str(e)
                        )
                    )
                    update_lock(event.chat_id, "bots", False)
                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(
                    users_added_by
                )
            )


CMD_HELP.update(
    {
        "locks": "**Plugin : **`locks`\
        \n\n**•  Syntax : **`.lock <all/type>`\
        \n•  **Function : **__Allows you to lock the permissions of the chat.__\
        \n\n**•  Syntax : **`.unlock <all/type>`\
        \n•  **Function : **__Allows you to unlock the permissions of the chat.__\
        \n\n•  **Syntax : **`.locks`\
        \n•  **Function : **__To see the active locks__\
        \n\n**•  Syntax : **`.plock <all/type>`\
        \n•  **Function : **__Allows you to lock the permissions of the replied user in that chat.__\
        \n\n**•  Syntax : **`.punlock <all/type>`\
        \n•  **Function : **__Allows you to unlock the permissions of the replied user in that chat.__\
        \n\n**•  Syntax : **`.uperm <reply/username>`\
        \n•  **Function : **__Shows you the admin rights if he is admin else will show his permissions in the chat__\
        \n\n•  **Note :** __Requires proper admin rights in the chat !! and DB Options are available only for lock and unlock commands.__\
        \n•  **Available message types to lock/unlock are: \
        \n•  API Options : **`msg`, `media`, `sticker`, `gif`, `preview` ,`game` ,`inline`, `poll`, `invite`, `pin`, `info`\
        \n**•  DB Options : **`bots`, `commands`, `email`, `forward`, `url`\
        "
    }
)
