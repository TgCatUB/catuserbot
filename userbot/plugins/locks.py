from telethon import events, functions, types
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from ..utils import admin_cmd, sudo_cmd
from . import CMD_HELP
from .sql_helper.locks_sql import get_locks, is_locked, update_lock


@bot.on(admin_cmd(pattern=r"lock( (?P<target>\S+)|$)"))
@bot.on(sudo_cmd(pattern=r"lock( (?P<target>\S+)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".lock"
    input_str = event.pattern_match.group("target")
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await edit_or_reply(event, "`Locked {}`".format(input_str))
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str == "msg":
            msg = True
            locktype = "messages"
        elif input_str == "media":
            media = True
            locktype = "media"
        elif input_str == "sticker":
            sticker = True
            locktype = "stickers"
        elif input_str == "gif":
            gif = True
            locktype = "GIFs"
        elif input_str == "game":
            gamee = True
            locktype = "games"
        elif input_str == "inline":
            ainline = True
            locktype = "inline bots"
        elif input_str == "poll":
            gpoll = True
            locktype = "polls"
        elif input_str == "invite":
            adduser = True
            locktype = "invites"
        elif input_str == "pin":
            cpin = True
            locktype = "pins"
        elif input_str == "info":
            changeinfo = True
            locktype = "chat info"
        elif input_str == "all":
            msg = True
            media = True
            sticker = True
            gif = True
            gamee = True
            ainline = True
            gpoll = True
            adduser = True
            cpin = True
            changeinfo = True
            locktype = "everything"
        else:
            if not input_str:
                return await edit_or_reply(event, "`I can't lock nothing !!`")
            else:
                return await edit_delete(
                    event, f"`Invalid lock type:` {input_str}", time=5
                )

        lock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
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
                f"`Do I have proper rights for that ??`\n**Error:** {str(e)}",
                time=5,
            )


@bot.on(admin_cmd(pattern="unlock (.*)"))
@bot.on(sudo_cmd(pattern="unlock (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await edit_or_reply(event, "`UnLocked {}`".format(input_str))
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str == "msg":
            msg = False
            locktype = "messages"
        elif input_str == "media":
            media = False
            locktype = "media"
        elif input_str == "sticker":
            sticker = False
            locktype = "stickers"
        elif input_str == "gif":
            gif = False
            locktype = "GIFs"
        elif input_str == "game":
            gamee = False
            locktype = "games"
        elif input_str == "inline":
            ainline = False
            locktype = "inline bots"
        elif input_str == "poll":
            gpoll = False
            locktype = "polls"
        elif input_str == "invite":
            adduser = False
            locktype = "invites"
        elif input_str == "pin":
            cpin = False
            locktype = "pins"
        elif input_str == "info":
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
            adduser = False
            cpin = False
            changeinfo = False
            locktype = "everything"
        else:
            if not input_str:
                return await edit_or_reply(event, "`I can't unlock nothing !!`")
            else:
                return await edit_delete(
                    event, f"`Invalid unlock type:` {input_str}", time=5
                )

        unlock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
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
                f"`Do I have proper rights for that ??`\n**Error:** {str(e)}",
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
        res = "There are no DataBase locks in this chat"
    else:
        res = "Following are the DataBase locks in this chat: \n"
        res += "👉 `bots`: `{}`\n".format(current_db_locks.bots)
        res += "👉 `commands`: `{}`\n".format(current_db_locks.commands)
        res += "👉 `email`: `{}`\n".format(current_db_locks.email)
        res += "👉 `forward`: `{}`\n".format(current_db_locks.forward)
        res += "👉 `url`: `{}`\n".format(current_db_locks.url)
    current_chat = await event.get_chat()
    try:
        current_api_locks = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        res += "\nFollowing are the API locks in this chat: \n"
        res += "👉 `msg`: `{}`\n".format(current_api_locks.send_messages)
        res += "👉 `media`: `{}`\n".format(current_api_locks.send_media)
        res += "👉 `sticker`: `{}`\n".format(current_api_locks.send_stickers)
        res += "👉 `gif`: `{}`\n".format(current_api_locks.send_gifs)
        res += "👉 `gamee`: `{}`\n".format(current_api_locks.send_games)
        res += "👉 `ainline`: `{}`\n".format(current_api_locks.send_inline)
        res += "👉 `gpoll`: `{}`\n".format(current_api_locks.send_polls)
        res += "👉 `adduser`: `{}`\n".format(current_api_locks.invite_users)
        res += "👉 `cpin`: `{}`\n".format(current_api_locks.pin_messages)
        res += "👉 `changeinfo`: `{}`\n".format(current_api_locks.change_info)
    await edit_or_reply(event, res)


@bot.on(events.MessageEdited())
@bot.on(events.NewMessage())
async def check_incoming_messages(event):
    # TODO: exempt admins from locks
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


@bot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # TODO: exempt admins from locks
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
        if Config.G_BAN_LOGGER_GROUP is not None and is_ban_able:
            ban_reason_msg = await event.reply(
                "!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(
                    users_added_by
                )
            )


CMD_HELP.update(
    {
        "locks": "**Plugin : **`locks`\
        \n\n**  •  Syntax : **`.lock <all (or) type(s)> or .unlock <all (or) type(s)>`\
        \n  •  **Function : **__Allows you to lock/unlock some common message types in the chat.\
        \n  •  [NOTE: Requires proper admin rights in the chat !!]__\
        \n\n  •  **Available message types to lock/unlock are: \
        \n  •  API Options : **msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo\
        \n**  •  DB Options : **bots, commands, email, forward, url\
        \n\n  •  **Syntax : **`.locks`\
        \n  •  **Function : **__To see the active locks__"
    }
)
