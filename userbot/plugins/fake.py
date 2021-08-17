import asyncio
from random import choice, randint

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="scam(?:\s|$)([\s\S]*)",
    command=("scam", plugin_category),
    info={
        "header": "To show fake actions for a paticular period of time",
        "description": "if time is not mentioned then it may choose random time 5 or 6 mintues for mentioning time use in seconds",
        "usage": [
            "{tr}scam <action> <time(in seconds)>",
            "{tr}scam <action>",
            "{tr}scam",
        ],
        "examples": "{tr}scam photo 300",
        "actions": [
            "typing",
            "contact",
            "game",
            "location",
            "voice",
            "round",
            "video",
            "photo",
            "document",
        ],
    },
)
async def _(event):
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
            scam_time = randint(300, 360)
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


@catub.cat_cmd(
    pattern="prankpromote(?:\s|$)([\s\S]*)",
    command=("prankpromote", plugin_category),
    info={
        "header": "To promote a person without admin rights",
        "note": "You need proper rights for this",
        "usage": [
            "{tr}prankpromote <userid/username/reply>",
            "{tr}prankpromote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To promote a person without admin rights"
    new_rights = ChatAdminRights(post_messages=True)
    catevent = await edit_or_reply(event, "`Promoting...`")
    user, rank = await get_user_from_event(event, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit("__I think you don't have permission to promote__")
    except Exception as e:
        return await edit_delete(catevent, f"__{e}__", time=10)
    await catevent.edit("`Promoted Successfully! Now gib Party`")


@catub.cat_cmd(
    pattern="padmin$",
    command=("padmin", plugin_category),
    info={
        "header": "Fun animation for faking user promotion",
        "description": "An animation that shows enabling all permissions to him that he is admin(fake promotion)",
        "usage": "{tr}padmin",
    },
    groups_only=True,
)
async def _(event):
    "Fun animation for faking user promotion."
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "`promoting.......`")
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
        f"**pRoMooTeD SuCcEsSfUlLy bY: {ALIVE_NAME}**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])
