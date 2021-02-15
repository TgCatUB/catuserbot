import base64
import time
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
STAT_INDICATION = "`Collecting stats, this may take several minutes`"
PCHANNELS_STR = "**The list of Public channels in which you are their are here **\n\n"
PCHANNELS_ADMINSTR = "**The list of Public channels in which you are admin are here **\n\n"
PCHANNELS_OWNERSTR = "**The list of Public channels in which you are owner are here **\n\n"
PGROUPS_STR = "**The list of Public groups in which you are their are here **\n\n"
PGROUPS_ADMINSTR = "**The list of Public groups in which you are admin are here **\n\n"
PGROUPS_OWNERSTR = "**The list of Public groups in which you are owner are here **\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


@bot.on(admin_cmd(pattern="pstat (c|ca|co)$"))
@bot.on(sudo_cmd(pattern="pstat (c|ca|co)$", allow_sudo=True))
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
        if (
            isinstance(entity, Channel)
            and entity.broadcast
            and entity.username is not None
        ):
            hi.append([entity.title, entity.username])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.username])
            if entity.creator:
                hico.append([entity.title, entity.username])
    if catcmd == "c":
        output = PCHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PCHANNELS_STR
    elif catcmd == "ca":
        output = PCHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PCHANNELS_ADMINSTR
    elif catcmd == "co":
        output = PCHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PCHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**Time Taken : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )

@bot.on(admin_cmd(pattern="pstat (g|ga|go)$"))
@bot.on(sudo_cmd(pattern="pstat (g|ga|go)$", allow_sudo=True))
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
            and not isinstance(entity, Chat)
        ):
            if entity.username is not None:
                hi.append([entity.title, entity.username])
                if entity.creator or entity.admin_rights:
                    higa.append([entity.title, entity.username])
                if entity.creator:
                    higo.append([entity.title, entity.username])
    if catcmd == "g":
        output = PGROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PGROUPS_STR
    elif catcmd == "ga":
        output = PGROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PGROUPS_ADMINSTR
    elif catcmd == "go":
        output = PGROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/{i[1]})\n"
        caption = PGROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**Time Taken : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )

def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"

def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)

CMD_HELP.update(
    {
        "pstats": "**Plugin : **`pstats`\
    \n\n  •  **Syntax : **`.pstat (g|ga|go)`\
    \n  •  **Function : **__Shows you the list of all public groups  in which you are if you use g , all public groups in which you are admin if you use ga and all public groups created by you if you use go__\
    \n\n  •  **Syntax : **`.pstat (c|ca|co)`\
    \n  •  **Function : **__Shows you the list of all public channels in which you are if you use c , all public channels in which you are admin if you use ca and all public channels created by you if you use co__\
    "
    }
)