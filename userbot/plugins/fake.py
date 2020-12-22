import asyncio
from datetime import datetime
from random import choice, randint

from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from . import ALIVE_NAME

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@bot.on(admin_cmd(pattern="scam(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="scam(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    options = [
        "typing",
        "contact",
        "game",
        "location",
        "voice",
        "round",
        "video",
        "photo",
        "document",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(300, 360)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(200, 300)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await edit_delete(event, "`Invalid Syntax !!`")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await asyncio.sleep(scam_time)
    except BaseException:
        return


@bot.on(admin_cmd(pattern="prankpromote ?(.*)"))
@bot.on(sudo_cmd(pattern="prankpromote ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    to_promote_id = None
    rights = ChatAdminRights(post_messages=True)
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
    elif input_str:
        to_promote_id = input_str
    try:
        await event.client(EditAdminRequest(event.chat_id, to_promote_id, rights, ""))
    except (Exception) as exc:
        await edit_or_reply(event, str(exc))
    else:
        await edit_or_reply(event, "Successfully Promoted")


@bot.on(admin_cmd(pattern=f"padmin$", outgoing=True))
@bot.on(sudo_cmd(pattern="padmin$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "promoting.......")
    animation_chars = [
        "**Promoting User As Admin...**",
        "**Enabling All Permissions To User...**",
        "**(1) Send Messages: ☑️**",
        "**(1) Send Messages: ✅**",
        "**(2) Send Media: ☑️**",
        "**(2) Send Media: ✅**",
        "**(3) Send Stickers & GIFs: ☑️**",
        "**(3) Send Stickers & GIFs: ✅**",
        "**(4) Send Polls: ☑️**",
        "**(4) Send Polls: ✅**",
        "**(5) Embed Links: ☑️**",
        "**(5) Embed Links: ✅**",
        "**(6) Add Users: ☑️**",
        "**(6) Add Users: ✅**",
        "**(7) Pin Messages: ☑️**",
        "**(7) Pin Messages: ✅**",
        "**(8) Change Chat Info: ☑️**",
        "**(8) Change Chat Info: ✅**",
        "**Permission Granted Successfully**",
        f"**pRoMooTeD SuCcEsSfUlLy bY: {DEFAULTUSER}**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])


CMD_HELP.update(
    {
        "fake": "**fake**\
    \n\n**Syntax :** `.scam <action> <time>` \
    \n**Usage : **Type .scam (action name) This shows the fake action in the group, The actions are typing ,contact ,game, location, voice, round, video,photo,document, cancel.\
    \n\n**Syntax :** `.prankpromote` reply to user to whom you want to prank promote\
    \n**Usage : **it promotes him to admin but he will not have any permission to take action that is he can see rection actions but cant take any admin action\
    \n\n**Syntax :** `.padmin`\
    \n**Usage : ** An animation that shows enabling all permissions to him that he is admin(fake promotion)\
    "
    }
)
