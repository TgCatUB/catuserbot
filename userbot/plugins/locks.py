import base64

from telethon import events, functions, types
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights

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
        res += "👉 `preview`: `{}`\n".format(current_api_locks.embed_links)
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
        if Config.BOTLOG_CHATID is not None and is_ban_able:
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
        \n  •  API Options : **msg, media, sticker, gif, preview ,gamee, ainline, gpoll, adduser, cpin, changeinfo\
        \n**  •  DB Options : **bots, commands, email, forward, url\
        \n\n  •  **Syntax : **`.locks`\
        \n  •  **Function : **__To see the active locks__"
    }
)
